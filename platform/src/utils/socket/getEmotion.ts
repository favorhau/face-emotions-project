import axios from "axios";


export const getEmotion = async (imgBase64: string) => {

    return await axios.post('/api/test', {
        data: imgBase64,
    });
}