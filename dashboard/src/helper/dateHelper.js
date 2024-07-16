export default (timestamp) => {
    const date = new Date(timestamp);
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    // Extracting parts of the date
    const month = months[date.getMonth()];
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear().toString().slice(-2);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');

    // Formatting the new date string
    return `${month} ${day} ${year} ${hours}:${minutes}`;
}

export const getDistance = (lastTime) => {
    const now = new Date();
    const nextMin = Math.floor(now.getMinutes() / 5 + 1) * 5;
    const nextTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), nextMin, 20, 0);
    return nextTime.getTime() - lastTime;
}