

export default async function getStream(){

    const constraints = {
        audio: false,
        video: true
    }
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        
        return stream
        // handleSuccess(stream);
        // e.target.disabled = true;
    } catch (e) {
        // handleError(e);
        console.error('open camera error', e,)
    }
}