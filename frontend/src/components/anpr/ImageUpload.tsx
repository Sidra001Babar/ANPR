import {
    Upload,
    Image as ImageIcon,
    Loader2,
    X,
    Sparkles,
} from "lucide-react";

import {
    useEffect,
    useRef,
    useState,
} from "react";

import {
    processImage,
} from "../../services/anprApi";

import type {
    ProcessImageResponse,
} from "../../types/anpr";


interface ImageUploadProps {

    onResult: (
        result: ProcessImageResponse
    ) => void;

    onProcessingChange?: (
        loading: boolean
    ) => void;
}


const MAX_FILE_SIZE =
    10 * 1024 * 1024;


export default function ImageUpload({

    onResult,

    onProcessingChange,

}: ImageUploadProps) {


    const inputRef =
        useRef<HTMLInputElement | null>(
            null
        );


    const [
        selectedFile,
        setSelectedFile,
    ] = useState<File | null>(null);


    const [
        previewUrl,
        setPreviewUrl,
    ] = useState<string | null>(null);


    const [
        loading,
        setLoading,
    ] = useState(false);


    const [
        error,
        setError,
    ] = useState<string>("");


    useEffect(() => {

        return () => {

            if (previewUrl) {

                URL.revokeObjectURL(
                    previewUrl
                );

            }

        };

    }, [previewUrl]);


    const handleFile = (
        file: File
    ) => {

        setError("");


        if (
            !file.type.startsWith(
                "image/"
            )
        ) {

            setError(
                "Please select a valid image file."
            );

            return;

        }


        if (
            file.size >
            MAX_FILE_SIZE
        ) {

            setError(
                "Image size must be less than 10 MB."
            );

            return;

        }


        if (previewUrl) {

            URL.revokeObjectURL(
                previewUrl
            );

        }


        const url =
            URL.createObjectURL(
                file
            );


        setSelectedFile(
            file
        );

        setPreviewUrl(
            url
        );

    };


    const handleFileChange = (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {

        const file =
            event.target.files?.[0];


        if (!file) {

            return;

        }


        handleFile(file);

    };


    const handleDrop = (
        event: React.DragEvent<HTMLDivElement>
    ) => {

        event.preventDefault();


        const file =
            event.dataTransfer.files?.[0];


        if (!file) {

            return;

        }


        handleFile(file);

    };


    const handleDragOver = (
        event: React.DragEvent<HTMLDivElement>
    ) => {

        event.preventDefault();

    };


    const clearFile = () => {

        if (previewUrl) {

            URL.revokeObjectURL(
                previewUrl
            );

        }


        setSelectedFile(null);

        setPreviewUrl(null);

        setError("");


        if (inputRef.current) {

            inputRef.current.value = "";

        }

    };


    const handleProcess = async () => {

        if (!selectedFile) {

            setError(
                "Please select an image first."
            );

            return;

        }


        try {

            setLoading(true);

            setError("");


            onProcessingChange?.(
                true
            );


            const result =
                await processImage(
                    selectedFile
                );


            onResult(result);

        } catch (err: unknown) {

            console.error(
                "ANPR processing error:",
                err
            );


            let message =
                "Failed to process the image.";


            if (
                typeof err ===
                "object" &&
                err !== null &&
                "response" in err
            ) {

                const axiosError =
                    err as {
                        response?: {
                            data?: {
                                detail?: string;
                            };
                        };
                    };


                message =
                    axiosError.response
                        ?.data
                        ?.detail ??
                    message;

            }


            setError(
                message
            );

        } finally {

            setLoading(false);

            onProcessingChange?.(
                false
            );

        }

    };


    return (

        <div
            className="
                space-y-5
            "
        >

            {/* Upload area */}

            {!selectedFile && (

                <div
                    onDrop={
                        handleDrop
                    }

                    onDragOver={
                        handleDragOver
                    }

                    onClick={() =>
                        inputRef.current?.click()
                    }

                    className="
                        group
                        cursor-pointer
                        rounded-2xl
                        border-2
                        border-dashed
                        border-gray-300
                        bg-gray-50
                        p-8
                        text-center
                        transition-all
                        duration-200
                        hover:border-blue-400
                        hover:bg-blue-50
                    "
                >

                    <input
                        ref={inputRef}
                        type="file"
                        accept="
                            image/jpeg,
                            image/png,
                            image/webp,
                            image/bmp
                        "
                        onChange={
                            handleFileChange
                        }
                        className="hidden"
                    />


                    <div
                        className="
                            mx-auto
                            flex
                            h-16
                            w-16
                            items-center
                            justify-center
                            rounded-2xl
                            bg-blue-100
                            text-blue-600
                            transition-transform
                            group-hover:scale-105
                        "
                    >

                        <Upload
                            size={28}
                        />

                    </div>


                    <h3
                        className="
                            mt-5
                            text-lg
                            font-semibold
                            text-gray-900
                        "
                    >
                        Drop your image here
                    </h3>


                    <p
                        className="
                            mt-2
                            text-sm
                            text-gray-500
                        "
                    >
                        or click to browse
                    </p>


                    <p
                        className="
                            mt-4
                            text-xs
                            text-gray-400
                        "
                    >
                        JPG, PNG, WEBP or BMP
                        {" • "}
                        Max 10 MB
                    </p>

                </div>

            )}


            {/* Preview */}

            {selectedFile &&
                previewUrl && (

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
                                px-4
                                py-3
                            "
                        >

                            <div
                                className="
                                    flex
                                    min-w-0
                                    items-center
                                    gap-3
                                "
                            >

                                <div
                                    className="
                                        flex
                                        h-9
                                        w-9
                                        shrink-0
                                        items-center
                                        justify-center
                                        rounded-lg
                                        bg-blue-50
                                        text-blue-600
                                    "
                                >

                                    <ImageIcon
                                        size={18}
                                    />

                                </div>


                                <div
                                    className="
                                        min-w-0
                                    "
                                >

                                    <p
                                        className="
                                            truncate
                                            text-sm
                                            font-semibold
                                            text-gray-800
                                        "
                                    >
                                        {
                                            selectedFile.name
                                        }
                                    </p>


                                    <p
                                        className="
                                            text-xs
                                            text-gray-500
                                        "
                                    >
                                        {(
                                            selectedFile.size /
                                            1024 /
                                            1024
                                        ).toFixed(2)}
                                        {" MB"}
                                    </p>

                                </div>

                            </div>


                            <button
                                type="button"
                                onClick={
                                    clearFile
                                }
                                disabled={
                                    loading
                                }
                                className="
                                    rounded-lg
                                    p-2
                                    text-gray-400
                                    transition
                                    hover:bg-gray-100
                                    hover:text-gray-700
                                    disabled:opacity-40
                                "
                            >

                                <X
                                    size={18}
                                />

                            </button>

                        </div>


                        <div
                            className="
                                bg-gray-100
                                p-3
                            "
                        >

                            <img
                                src={previewUrl}
                                alt="Selected vehicle"
                                className="
                                    max-h-[500px]
                                    w-full
                                    rounded-xl
                                    object-contain
                                "
                            />

                        </div>

                    </div>

                )}


            {/* Error */}

            {error && (

                <div
                    className="
                        rounded-xl
                        border
                        border-red-200
                        bg-red-50
                        px-4
                        py-3
                        text-sm
                        text-red-600
                    "
                >
                    {error}
                </div>

            )}


            {/* Process button */}

            <button
                type="button"
                disabled={
                    !selectedFile ||
                    loading
                }
                onClick={
                    handleProcess
                }
                className="
                    flex
                    w-full
                    items-center
                    justify-center
                    gap-2
                    rounded-xl
                    bg-blue-600
                    px-5
                    py-3.5
                    font-semibold
                    text-white
                    shadow-sm
                    transition-all
                    hover:bg-blue-700
                    hover:shadow-md
                    disabled:cursor-not-allowed
                    disabled:opacity-50
                "
            >

                {loading ? (

                    <>
                        <Loader2
                            size={19}
                            className="
                                animate-spin
                            "
                        />

                        Processing ANPR...
                    </>

                ) : (

                    <>
                        <Sparkles
                            size={19}
                        />

                        Process Image
                    </>

                )}

            </button>

        </div>

    );

}