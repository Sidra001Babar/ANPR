import axios from "axios";

import type {
    ProcessImageResponse,
} from "../types/anpr";


const API_BASE_URL =
    "http://127.0.0.1:8000";


const api = axios.create({

    baseURL: API_BASE_URL,

});


export const processImage = async (
    file: File,
): Promise<ProcessImageResponse> => {

    const formData = new FormData();

    formData.append(
        "file",
        file,
    );


    const response =
        await api.post<ProcessImageResponse>(
            "/api/image/process",
            formData,
        );


    return response.data;
};


export const getProcessedImageUrl = (
    path: string,
): string => {

    return `${API_BASE_URL}${path}`;

};