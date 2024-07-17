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

export const getTimeDiff = () => {
    const now = new Date();
    const lastMin = Math.floor(now.getMinutes() / 5) * 5;
    console.log(lastMin);
    const lastTime = new Date();
    lastTime.setMinutes(lastMin, 0, 0);
    console.log(lastTime);
    if (now.getTime() - lastTime.getTime() < 10000) {
        return 10000 - now.getTime() + lastTime.getTime();
    }

    lastTime.setMinutes(lastMin + 5, 10);
    return lastTime.getTime() - now.getTime();
}