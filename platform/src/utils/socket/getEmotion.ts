import axios from "axios";


export const getEmotion = async () => {

    return await axios.post('/api/test');
}