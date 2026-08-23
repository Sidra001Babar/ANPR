import re
from collections import Counter
import easyocr
from app.config import (
    OCR_LANGUAGE,
    OCR_MIN_CONFIDENCE,
)
class PlateOCR:
    def __init__(self):
        print(
            "Loading EasyOCR..."
        )
        self.reader = easyocr.Reader(
            OCR_LANGUAGE,
            gpu=False,
        )
        print(
            "EasyOCR loaded."
        )
    # NORMALIZE TEXT
    @staticmethod
    def normalize_text(text):
        if not text:
            return ""
        text = text.upper()
        text = re.sub(
            r"[^A-Z0-9]",
            "",
            text,
        )
        return text
    # VALIDATE BASIC CANDIDATE
    @staticmethod
    def is_valid_candidate(text):
        if not text:
            return False
        length = len(text)
        if length < 4 or length > 12:
            return False
        has_letter = any(
            char.isalpha()
            for char in text
        )
        has_number = any(
            char.isdigit()
            for char in text
        )
        if not has_letter:
            return False

        if not has_number:
            return False

        return True
    # READ ONE IMAGE
    def _read_single(self, image):
        try:
            results = self.reader.readtext(
                image,
                detail=1,
                paragraph=False,
                allowlist=(
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    "0123456789"
                ),
                mag_ratio=1.0,
            )
        except Exception as error:
            print(
                "EasyOCR error:",
                error,
            )
            return []
        candidates = []
        for result in results:
            if len(result) != 3:
                continue
            bbox, text, confidence = result
            text = self.normalize_text(
                text
            )
            if not text:
                continue
            confidence = float(
                confidence
            )
            candidates.append(
                {
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox,
                }
            )
        return candidates
    # COMBINE OCR REGIONS
    @staticmethod
    def combine_regions(results):
        if not results:
            return None, 0
        sorted_results = sorted(
            results,
            key=lambda item: min(
                point[0]
                for point in item["bbox"]
            ),
        )
        texts = [
            item["text"]
            for item in sorted_results
        ]
        confidences = [
            item["confidence"]
            for item in sorted_results
        ]
        combined = "".join(texts)
        if not combined:
            return None, 0
        average_confidence = (
            sum(confidences)
            / len(confidences)
        )
        return (
            combined,
            average_confidence,
        )
    # GENERATE CANDIDATES
    def _generate_candidates(
        self,
        processed_variants,
    ):
        candidates = []
        for variant_name, image in (
            processed_variants.items()
        ):
            results = self._read_single(
                image
            )
            if not results:
                continue
            combined_text, confidence = (
                self.combine_regions(
                    results
                )
            )
            if not combined_text:
                continue
            if not self.is_valid_candidate(
                combined_text
            ):
                continue
            candidates.append(
                {
                    "text": combined_text,
                    "confidence": confidence,
                    "variant": variant_name,
                }
            )
            print(
                f"OCR [{variant_name}]: "
                f"{combined_text} "
                f"({confidence * 100:.2f}%)"
            )
        return candidates
    # SIMILARITY
    @staticmethod
    def character_similarity(
        text_a,
        text_b,
    ):
        if not text_a or not text_b:
            return 0.0
        max_length = max(
            len(text_a),
            len(text_b),
        )
        min_length = min(
            len(text_a),
            len(text_b),
        )
        matches = sum(
            1
            for i in range(min_length)
            if text_a[i] == text_b[i]
        )
        return matches / max_length
    # CONSISTENCY SCORE
    def _consistency_score(
        self,
        candidate,
        candidates,
    ):
        score = 0.0
        for other in candidates:
            if other is candidate:
                continue
            similarity = (
                self.character_similarity(
                    candidate["text"],
                    other["text"],
                )
            )
            score += similarity
        return score
    # FINAL SELECTION
    def _select_best_candidate(
        self,
        candidates,
    ):
        if not candidates:
            return (
                "Unreadable",
                0,
            )
        # Count exact repetitions
        counts = Counter(
            candidate["text"]
            for candidate in candidates
        )
        # Score every candidate
        scored = []
        for candidate in candidates:
            text = candidate["text"]
            confidence = (
                candidate["confidence"]
            )
            frequency = counts[text]
            consistency = (
                self._consistency_score(
                    candidate,
                    candidates,
                )
            )
            length = len(text)
            if length >= 8:
                length_score = 1.0
            elif length >= 6:
                length_score = 0.7
            elif length >= 5:
                length_score = 0.4
            else:
                length_score = 0.1
            # Final score
            score = (
                confidence * 0.45
                +
                min(
                    consistency / max(
                        len(candidates) - 1,
                        1,
                    ),
                    1.0,
                ) * 0.30
                +
                min(
                    frequency / 3.0,
                    1.0,
                ) * 0.15
                +
                length_score * 0.10
            )
            scored.append(
                {
                    "candidate": candidate,
                    "score": score,
                }
            )
        # Select final candidate
        best = max(
            scored,
            key=lambda item: item["score"],
        )
        best_candidate = best[
            "candidate"
        ]
        final_text = best_candidate[
            "text"
        ]
        final_confidence = (
            best_candidate[
                "confidence"
            ] * 100
        )
        print(
            "\nOCR candidate scoring:"
        )
        for item in sorted(
            scored,
            key=lambda x: x["score"],
            reverse=True,
        ):
            candidate = item[
                "candidate"
            ]
            print(
                f"  "
                f"{candidate['text']} "
                f"| OCR="
                f"{candidate['confidence'] * 100:.2f}% "
                f"| score="
                f"{item['score']:.3f}"
            )
        return (
            final_text,
            final_confidence,
        )

    # PUBLIC OCR METHOD
    def extract_text(
        self,
        processed_variants,
    ):
        candidates = (
            self._generate_candidates(
                processed_variants
            )
        )
        if not candidates:

            return (
                "Unreadable",
                0,
            )
        return self._select_best_candidate(
            candidates
        )