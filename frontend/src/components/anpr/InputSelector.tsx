import {
    Image,
    Video,
    Camera,
} from "lucide-react";


export type InputMode =
    | "image"
    | "video"
    | "webcam";


interface InputSelectorProps {

    activeMode: InputMode;

    onChange: (
        mode: InputMode
    ) => void;
}


interface InputOption {

    id: InputMode;

    label: string;

    description: string;

    icon: typeof Image;

    enabled: boolean;
}


const options: InputOption[] = [

    {
        id: "image",

        label: "Upload Image",

        description:
            "Analyze a vehicle image",

        icon: Image,

        enabled: true,
    },

    {
        id: "video",

        label: "Upload Video",

        description:
            "Coming in the next step",

        icon: Video,

        enabled: false,
    },

    {
        id: "webcam",

        label: "Live Webcam",

        description:
            "Coming in the next step",

        icon: Camera,

        enabled: false,
    },

];


export default function InputSelector({

    activeMode,

    onChange,

}: InputSelectorProps) {


    return (

        <div
            className="
                grid
                grid-cols-1
                gap-3
                sm:grid-cols-3
            "
        >

            {options.map((option) => {

                const Icon =
                    option.icon;

                const isActive =
                    activeMode === option.id;


                return (

                    <button
                        key={option.id}

                        type="button"

                        disabled={
                            !option.enabled
                        }

                        onClick={() => {

                            if (
                                option.enabled
                            ) {

                                onChange(
                                    option.id
                                );

                            }

                        }}

                        className={`
                            group
                            rounded-2xl
                            border
                            p-4
                            text-left
                            transition-all
                            duration-200

                            ${
                                isActive
                                    ? `
                                        border-blue-500
                                        bg-blue-50
                                        shadow-sm
                                      `
                                    : `
                                        border-gray-200
                                        bg-white
                                      `
                            }

                            ${
                                option.enabled
                                    ? `
                                        cursor-pointer
                                        hover:-translate-y-0.5
                                        hover:border-blue-400
                                        hover:shadow-md
                                      `
                                    : `
                                        cursor-not-allowed
                                        opacity-45
                                      `
                            }
                        `}
                    >

                        <div
                            className="
                                flex
                                items-start
                                justify-between
                            "
                        >

                            <div
                                className={`
                                    flex
                                    h-11
                                    w-11
                                    items-center
                                    justify-center
                                    rounded-xl

                                    ${
                                        isActive
                                            ? `
                                                bg-blue-600
                                                text-white
                                              `
                                            : `
                                                bg-gray-100
                                                text-gray-600
                                              `
                                    }
                                `}
                            >

                                <Icon
                                    size={21}
                                />

                            </div>


                            {!option.enabled && (

                                <span
                                    className="
                                        rounded-full
                                        bg-gray-100
                                        px-2.5
                                        py-1
                                        text-[10px]
                                        font-semibold
                                        uppercase
                                        tracking-wide
                                        text-gray-500
                                    "
                                >
                                    Soon
                                </span>

                            )}

                        </div>


                        <div
                            className="mt-4"
                        >

                            <h3
                                className="
                                    font-semibold
                                    text-gray-900
                                "
                            >
                                {option.label}
                            </h3>


                            <p
                                className="
                                    mt-1
                                    text-xs
                                    leading-5
                                    text-gray-500
                                "
                            >
                                {
                                    option.description
                                }
                            </p>

                        </div>

                    </button>

                );

            })}

        </div>

    );

}