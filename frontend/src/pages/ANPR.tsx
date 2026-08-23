import {
    ShieldCheck,
    Cpu,
} from "lucide-react";

import {
    useState,
} from "react";


import InputSelector, {
    type InputMode,
} from "../components/anpr/InputSelector";


import ImageUpload from "../components/anpr/ImageUpload";


import ResultPanel from "../components/anpr/ResultPanel";


import type {
    ProcessImageResponse,
} from "../types/anpr";


export default function ANPR() {


    const [
        mode,
        setMode,
    ] = useState<InputMode>(
        "image"
    );


    const [
        result,
        setResult,
    ] = useState<ProcessImageResponse | null>(
        null
    );


    const [
        processing,
        setProcessing,
    ] = useState(false);


    return (

        <main
            className="
                min-h-screen
                bg-gradient-to-br
                from-slate-50
                via-white
                to-blue-50
                px-4
                py-8
                sm:px-6
                lg:px-8
            "
        >

            <div
                className="
                    mx-auto
                    max-w-7xl
                "
            >

                {/* Header */}

                <header
                    className="
                        mb-8
                        text-center
                    "
                >

                    <div
                        className="
                            mx-auto
                            flex
                            w-fit
                            items-center
                            gap-2
                            rounded-full
                            border
                            border-blue-100
                            bg-blue-50
                            px-4
                            py-2
                            text-xs
                            font-semibold
                            text-blue-700
                        "
                    >

                        <ShieldCheck
                            size={16}
                        />

                        AI-Powered ANPR

                    </div>


                    <h1
                        className="
                            mt-5
                            text-3xl
                            font-bold
                            tracking-tight
                            text-slate-900
                            sm:text-4xl
                            lg:text-5xl
                        "
                    >
                        Automatic Number
                        <span
                            className="
                                text-blue-600
                            "
                        >
                            {" "}Plate Recognition
                        </span>
                    </h1>


                    <p
                        className="
                            mx-auto
                            mt-4
                            max-w-2xl
                            text-sm
                            leading-6
                            text-slate-500
                            sm:text-base
                        "
                    >
                        Upload an image to detect
                        vehicles and recognize
                        license plates using the
                        ANPR processing pipeline.
                    </p>

                </header>


                {/* Input mode selector */}

                <section
                    className="
                        rounded-2xl
                        border
                        border-slate-200
                        bg-white
                        p-4
                        shadow-sm
                        sm:p-5
                    "
                >

                    <div
                        className="
                            mb-4
                            flex
                            items-center
                            gap-2
                        "
                    >

                        <Cpu
                            size={18}
                            className="text-blue-600"
                        />


                        <h2
                            className="
                                text-sm
                                font-semibold
                                text-slate-800
                            "
                        >
                            Choose input source
                        </h2>

                    </div>


                    <InputSelector
                        activeMode={mode}
                        onChange={
                            setMode
                        }
                    />

                </section>


                {/* Main workspace */}

                {mode === "image" && (

                    <section
                        className="
                            mt-6
                            grid
                            gap-6
                            lg:grid-cols-2
                            lg:items-start
                        "
                    >

                        {/* Upload */}

                        <div
                            className="
                                rounded-2xl
                                border
                                border-slate-200
                                bg-white
                                p-5
                                shadow-sm
                                sm:p-6
                            "
                        >

                            <div
                                className="
                                    mb-5
                                "
                            >

                                <h2
                                    className="
                                        text-lg
                                        font-semibold
                                        text-slate-900
                                    "
                                >
                                    Image Analysis
                                </h2>


                                <p
                                    className="
                                        mt-1
                                        text-sm
                                        text-slate-500
                                    "
                                >
                                    Select a vehicle
                                    image and run
                                    ANPR detection.
                                </p>

                            </div>


                            <ImageUpload
                                onResult={
                                    setResult
                                }
                                onProcessingChange={
                                    setProcessing
                                }
                            />

                        </div>


                        {/* Result */}

                        <div>

                            <ResultPanel
                                response={
                                    result
                                }
                            />

                        </div>

                    </section>

                )}


                {/* Future modes */}

                {mode === "video" && (

                    <ComingSoon
                        title="Video ANPR"
                        description="
                            Video upload and
                            frame-by-frame ANPR
                            processing will be
                            implemented next.
                        "
                    />

                )}


                {mode === "webcam" && (

                    <ComingSoon
                        title="Live Webcam"
                        description="
                            Real-time webcam
                            detection will be
                            implemented after
                            video processing.
                        "
                    />

                )}


                {/* Processing indicator */}

                {processing && (

                    <div
                        className="
                            pointer-events-none
                            fixed
                            bottom-5
                            left-1/2
                            z-50
                            -translate-x-1/2
                            rounded-full
                            border
                            border-blue-100
                            bg-white
                            px-5
                            py-3
                            text-sm
                            font-semibold
                            text-blue-700
                            shadow-lg
                        "
                    >
                        Processing image...
                    </div>

                )}

            </div>

        </main>

    );

}


interface ComingSoonProps {

    title: string;

    description: string;

}


function ComingSoon({

    title,

    description,

}: ComingSoonProps) {


    return (

        <section
            className="
                mt-6
                flex
                min-h-[400px]
                items-center
                justify-center
                rounded-2xl
                border-2
                border-dashed
                border-slate-200
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
                        bg-blue-50
                        text-blue-600
                    "
                >

                    <Cpu
                        size={28}
                    />

                </div>


                <h2
                    className="
                        mt-5
                        text-xl
                        font-bold
                        text-slate-900
                    "
                >
                    {title}
                </h2>


                <p
                    className="
                        mx-auto
                        mt-2
                        max-w-md
                        text-sm
                        leading-6
                        text-slate-500
                    "
                >
                    {description}
                </p>

            </div>

        </section>

    );

}