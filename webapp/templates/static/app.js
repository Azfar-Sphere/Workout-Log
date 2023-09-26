// Checks for indexedDB support
if (!('indexedDB' in window)) {
    console.log("This browser doesn't support IndexedDB");
    return;
}