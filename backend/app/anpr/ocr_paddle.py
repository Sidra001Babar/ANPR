import re
from collections import Counter

import cv2
from paddleocr import PaddleOCR

from app.config import OCR_MIN_CONFIDENCE


class PlateOCR:
    def __init__(self):
        print("Loading PaddleOCR...")
        self.reader = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,   # <-- CHANGED: avoids the oneDNN crash
            lang="en",
            enable_mkldnn=False, 
        )
        print("PaddleOCR loaded.")

    @staticmethod
    def normalize_text(text):
        if not text:
            return ""
        text = text.upper()
        text = re.sub(r"[^A-Z0-9]", "", text)
        return text

    @staticmethod
    def is_valid_candidate(text):
        if not text:
            return False
        length = len(text)
        if length < 4 or length > 12:
            return False
        has_letter = any(c.isalpha() for c in text)
        has_number = any(c.isdigit() for c in text)
        return has_letter and has_number

    @staticmethod
    def _ensure_bgr(image):
        # PaddleOCR's predict() expects a 3-channel image.
        # Our grayscale/binarized variants are 2D, so convert them back.
        if image is None:
            return None
        if image.ndim == 2:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        return image

    def _read_single(self, image):
        image = self._ensure_bgr(image)
        if image is None:
            return []

        try:
            results = self.reader.predict(image)
        except Exception as error:
            print("PaddleOCR error:", error)
            return []

        candidates = []
        for res in results:
            try:
                rec_texts = res["rec_texts"]
                rec_scores = res["rec_scores"]
                rec_polys = res.get("rec_polys") or res.get("dt_polys") or []
            except Exception as error:
                print("PaddleOCR result parse error:", error)
                continue

            for i, text in enumerate(rec_texts):
                text = self.normalize_text(text)
                if not text:
                    continue
                confidence = float(rec_scores[i]) if i < len(rec_scores) else 0.0
                bbox = rec_polys[i] if i < len(rec_polys) else [[0, 0]]
                candidates.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox,
                })
        return candidates

    @staticmethod
    def combine_regions(results):
        if not results:
            return None, 0
        sorted_results = sorted(
            results,
            key=lambda item: min(point[0] for point in item["bbox"]),
        )
        texts = [item["text"] for item in sorted_results]
        confidences = [item["confidence"] for item in sorted_results]
        combined = "".join(texts)
        if not combined:
            return None, 0
        average_confidence = sum(confidences) / len(confidences)
        return combined, average_confidence

    def _generate_candidates(self, processed_variants):
        candidates = []
        for variant_name, image in processed_variants.items():
            results = self._read_single(image)
            if not results:
                continue
            combined_text, confidence = self.combine_regions(results)
            if not combined_text:
                continue
            if not self.is_valid_candidate(combined_text):
                continue
            candidates.append({
                "text": combined_text,
                "confidence": confidence,
                "variant": variant_name,
            })
            print(f"OCR [{variant_name}]: {combined_text} ({confidence * 100:.2f}%)")
        return candidates

    @staticmethod
    def character_similarity(text_a, text_b):
        if not text_a or not text_b:
            return 0.0
        max_length = max(len(text_a), len(text_b))
        min_length = min(len(text_a), len(text_b))
        matches = sum(1 for i in range(min_length) if text_a[i] == text_b[i])
        return matches / max_length

    def _consistency_score(self, candidate, candidates):
        score = 0.0
        for other in candidates:
            if other is candidate:
                continue
            score += self.character_similarity(candidate["text"], other["text"])
        return score

    def _select_best_candidate(self, candidates):
        if not candidates:
            return "Unreadable", 0

        counts = Counter(c["text"] for c in candidates)
        scored = []
        for candidate in candidates:
            text = candidate["text"]
            confidence = candidate["confidence"]
            frequency = counts[text]
            consistency = self._consistency_score(candidate, candidates)
            length = len(text)
            if length >= 8:
                length_score = 1.0
            elif length >= 6:
                length_score = 0.7
            elif length >= 5:
                length_score = 0.4
            else:
                length_score = 0.1

            score = (
                confidence * 0.45
                + min(consistency / max(len(candidates) - 1, 1), 1.0) * 0.30
                + min(frequency / 3.0, 1.0) * 0.15
                + length_score * 0.10
            )
            scored.append({"candidate": candidate, "score": score})

        best = max(scored, key=lambda item: item["score"])
        best_candidate = best["candidate"]
        final_text = best_candidate["text"]
        final_confidence = best_candidate["confidence"] * 100

        print("\nOCR candidate scoring:")
        for item in sorted(scored, key=lambda x: x["score"], reverse=True):
            c = item["candidate"]
            print(f"  {c['text']} | OCR={c['confidence'] * 100:.2f}% | score={item['score']:.3f}")

        return final_text, final_confidence

    def extract_text(self, processed_variants):
        candidates = self._generate_candidates(processed_variants)
        if not candidates:
            return "Unreadable", 0
        return self._select_best_candidate(candidates)