import {
    CheckCircle2,
    AlertCircle,
    CarFront,
    ScanLine,
} from "lucide-react";


import {
    getProcessedImageUrl,
} from "../../services/anprApi";


import type {
    ProcessImageResponse,
    VehicleResult,
} from "../../types/anpr";


interface ResultPanelProps {

    response:
        | ProcessImageResponse
        | null;

}


export default function ResultPanel({

    response,

}: ResultPanelProps) {


    if (!response) {

        return (

            <div
                className="
                    flex
                    min-h-[430px]
                    items-center
                    justify-center
                    rounded-2xl
                    border-2
                    border-dashed
                    border-gray-200
                    bg-white
                    p-8
                    text-center
                "
            >

                <div>

                    <div
                        className="
                            mx-auto
                            flex
                            h-16
                            w-16
                            items-center
                            justify-center
                            rounded-2xl
                            bg-gray-100
                            text-gray-400
                        "
                    >

                        <ScanLine
                            size={28}
                        />

                    </div>


                    <h3
                        className="
                            mt-5
                            font-semibold
                            text-gray-800
                        "
                    >
                        Your result will appear here
                    </h3>


                    <p
                        className="
                            mx-auto
                            mt-2
                            max-w-xs
                            text-sm
                            leading-6
                            text-gray-500
                        "
                    >
                        Upload a vehicle image
                        and start ANPR processing
                        to see the detected
                        license plates.
                    </p>

                </div>

            </div>

        );

    }


    const vehicles =
        response.result?.vehicles ?? [];


    const processedImageUrl =
        getProcessedImageUrl(
            response.processed_image
        );


const readableCount =
    vehicles.filter(
        (vehicle) =>
            vehicle.status === "Readable" &&
            vehicle.plate_text !== "Unreadable" &&
            vehicle.ocr_confidence >= 40
    ).length;


const unreadableCount =
    vehicles.filter(
        (vehicle) =>
            vehicle.status === "Unreadable" ||
            vehicle.plate_text === "Unreadable" ||
            vehicle.ocr_confidence < 40
    ).length;
    return (

        <div
            className="
                space-y-5
            "
        >

            {/* Processed image */}

            <div
                className="
                    overflow-hidden
                    rounded-2xl
                    border
                    bg-white
                    shadow-sm
                "
            >

                <div
                    className="
                        flex
                        items-center
                        justify-between
                        border-b
                        px-5
                        py-4
                    "
                >

                    <div>

                        <h2
                            className="
                                font-semibold
                                text-gray-900
                            "
                        >
                            Processed Result
                        </h2>


                        <p
                            className="
                                mt-1
                                text-xs
                                text-gray-500
                            "
                        >
                            Annotated ANPR output
                        </p>

                    </div>


                    <div
                        className="
                            flex
                            items-center
                            gap-1.5
                            rounded-full
                            bg-green-50
                            px-3
                            py-1.5
                            text-xs
                            font-semibold
                            text-green-700
                        "
                    >

                        <CheckCircle2
                            size={14}
                        />

                        Processed

                    </div>

                </div>


                <div
                    className="
                        bg-gray-100
                        p-3
                    "
                >

                    <img
                        src={processedImageUrl}
                        alt="Processed ANPR result"
                        className="
                            max-h-[600px]
                            w-full
                            rounded-xl
                            object-contain
                        "
                    />

                </div>

            </div>


            {/* Summary */}

            <div
                className="
                    grid
                    grid-cols-2
                    gap-3
                    sm:grid-cols-3
                "
            >

                <SummaryCard
                    label="Vehicles"
                    value={
                        vehicles.length
                    }
                    icon={
                        <CarFront
                            size={18}
                        />
                    }
                />


                <SummaryCard
                    label="Readable"
                    value={
                        readableCount
                    }
                    icon={
                        <CheckCircle2
                            size={18}
                        />
                    }
                />


                <SummaryCard
                    label="Unreadable"
                    value={
                        unreadableCount
                    }
                    icon={
                        <AlertCircle
                            size={18}
                        />
                    }
                />

            </div>


            {/* Vehicle results */}

            <div
                className="
                    rounded-2xl
                    border
                    bg-white
                    p-5
                    shadow-sm
                "
            >

                <div
                    className="
                        flex
                        items-center
                        justify-between
                    "
                >

                    <div>

                        <h2
                            className="
                                text-lg
                                font-semibold
                                text-gray-900
                            "
                        >
                            Detection Results
                        </h2>


                        <p
                            className="
                                mt-1
                                text-xs
                                text-gray-500
                            "
                        >
                            License plate information
                        </p>

                    </div>

                </div>


                {vehicles.length === 0 ? (

                    <div
                        className="
                            mt-5
                            flex
                            items-start
                            gap-3
                            rounded-xl
                            border
                            border-yellow-200
                            bg-yellow-50
                            p-4
                            text-sm
                            text-yellow-700
                        "
                    >

                        <AlertCircle
                            size={20}
                            className="mt-0.5 shrink-0"
                        />

                        <div>

                            <p
                                className="
                                    font-semibold
                                "
                            >
                                No license plate detected
                            </p>

                            <p
                                className="
                                    mt-1
                                    text-xs
                                "
                            >
                                No vehicle with a
                                detected license plate
                                was returned.
                            </p>

                        </div>

                    </div>

                ) : (

                    <div
                        className="
                            mt-5
                            space-y-3
                        "
                    >

                        {vehicles.map(
                            (
                                vehicle
                            ) => (

                                <VehicleCard
                                    key={
                                        vehicle.vehicle_id
                                    }
                                    vehicle={
                                        vehicle
                                    }
                                />

                            )
                        )}

                    </div>

                )}

            </div>

        </div>

    );

}


interface SummaryCardProps {

    label: string;

    value: number;

    icon: React.ReactNode;

}


function SummaryCard({

    label,

    value,

    icon,

}: SummaryCardProps) {


    return (

        <div
            className="
                rounded-xl
                border
                bg-white
                p-4
                shadow-sm
            "
        >

            <div
                className="
                    flex
                    items-center
                    gap-2
                    text-gray-500
                "
            >

                {icon}

                <span
                    className="
                        text-xs
                        font-medium
                    "
                >
                    {label}
                </span>

            </div>


            <p
                className="
                    mt-2
                    text-2xl
                    font-bold
                    text-gray-900
                "
            >
                {value}
            </p>

        </div>

    );

}


interface VehicleCardProps {

    vehicle: VehicleResult;

}


function VehicleCard({

    vehicle,

}: VehicleCardProps) {


    const isReadable =
        vehicle.status ===
        "Readable";


    return (

        <div
            className="
                rounded-xl
                border
                p-4
                transition
                hover:shadow-sm
            "
        >

            <div
                className="
                    flex
                    items-center
                    justify-between
                    gap-3
                "
            >

                <div
                    className="
                        flex
                        items-center
                        gap-3
                    "
                >

                    <div
                        className="
                            flex
                            h-10
                            w-10
                            items-center
                            justify-center
                            rounded-lg
                            bg-blue-50
                            text-blue-600
                        "
                    >

                        <CarFront
                            size={20}
                        />

                    </div>


                    <div>

                        <p
                            className="
                                font-semibold
                                capitalize
                                text-gray-900
                            "
                        >
                            {
                                vehicle.vehicle_class
                            }
                        </p>


                        <p
                            className="
                                text-xs
                                text-gray-500
                            "
                        >
                            Vehicle #
                            {
                                vehicle.vehicle_id
                            }
                        </p>

                    </div>

                </div>


                <span
                    className={`
                        rounded-full
                        px-3
                        py-1
                        text-xs
                        font-semibold

                        ${
                            isReadable
                                ? `
                                    bg-green-50
                                    text-green-700
                                  `
                                : `
                                    bg-yellow-50
                                    text-yellow-700
                                  `
                        }
                    `}
                >
                    {
                        vehicle.status
                    }
                </span>

            </div>


            <div
                className="
                    mt-4
                    grid
                    grid-cols-1
                    gap-3
                    sm:grid-cols-3
                "
            >

                <InfoItem
                    label="Plate Number"
                    value={
                        vehicle.plate_text
                    }
                    highlight
                />


                <InfoItem
                    label="Vehicle Confidence"
                    value={`
                        ${(
                            vehicle.vehicle_confidence *
                            100
                        ).toFixed(1)}%
                    `}
                />


                <InfoItem
                    label="OCR Confidence"
                    value={`
                        ${Number(
                            vehicle.ocr_confidence
                        ).toFixed(1)}%
                    `}
                />

            </div>


            {vehicle.reason && (

                <p
                    className="
                        mt-3
                        text-xs
                        text-gray-500
                    "
                >
                    {vehicle.reason}
                </p>

            )}

        </div>

    );

}


interface InfoItemProps {

    label: string;

    value: string;

    highlight?: boolean;

}


function InfoItem({

    label,

    value,

    highlight = false,

}: InfoItemProps) {


    return (

        <div
            className="
                rounded-lg
                bg-gray-50
                p-3
            "
        >

            <p
                className="
                    text-[11px]
                    font-medium
                    uppercase
                    tracking-wide
                    text-gray-400
                "
            >
                {label}
            </p>


            <p
                className={`
                    mt-1
                    break-all
                    ${
                        highlight
                            ? `
                                text-base
                                font-bold
                                tracking-wide
                                text-blue-600
                              `
                            : `
                                text-sm
                                font-semibold
                                text-gray-800
                              `
                    }
                `}
            >
                {value}
            </p>

        </div>

    );

}