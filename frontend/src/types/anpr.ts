export type ANPRStatus =
    | "Readable"
    | "Unreadable";


export interface VehicleResult {

    vehicle_id: number;

    vehicle_class: string;

    vehicle_confidence: number;

    vehicle_bbox: number[];

    plate_detected: boolean;

    plate_confidence: number;

    plate_bbox: number[] | null;

    vehicle_crop: string | null;

    plate_crop: string | null;

    processed_plate: string | null;

    plate_text: string;

    ocr_confidence: number;

    status: ANPRStatus;

    reason: string | null;
}


export interface ANPRResult {

    image: string;

    status: string;

    vehicles: VehicleResult[];

    output_image: string;
}


export interface ProcessImageResponse {

    success: boolean;

    message: string;

    filename: string;

    result: ANPRResult;

    processed_image: string;
}