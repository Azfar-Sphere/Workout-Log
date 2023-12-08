function confirmLogout() {
    var confirmation = confirm("Are you sure want to logout?");

    if (confirmation) {
        window.location.href = "/logout";
        return true;
    }
    else {
        return false;
    }
};