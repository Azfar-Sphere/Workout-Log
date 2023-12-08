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

function confirmDeleteSets() {
    var confirmation = confirm("Are you sure you want to delete your sets?");

    if (confirmation) {
        return true;
    }
    else {
        return false;
    }
};

function confirmWeek() {
    var confirmation = confirm("Are you sure you want to increment the week? This action cannot be reversed!");

    if (confirmation) {
        return true;
    }
    else {
        return false;
    }
};

function confirmDeleteExercise(day, exercise) {
    var confirmation = confirm("Are you sure you want to delete this exercise?");

    if (confirmation) {
        window.location.href = "/delete_e/" + day + "/" + exercise;
        return true;
    }
    else {
        return false;
    }
};
