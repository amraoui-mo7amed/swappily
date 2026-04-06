function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function t(key, fallback) {
    if (typeof translations !== "undefined" && translations[key]) {
        return translations[key];
    }
    return fallback;
}

document.addEventListener("DOMContentLoaded", function () {
    const skillForm = document.getElementById("skillForm");
    const swapRequestForm = document.getElementById("swapRequestForm");
    const deleteSkillBtn = document.getElementById("deleteSkillBtn");

    if (skillForm) {
        skillForm.addEventListener("submit", handleSkillFormSubmit);
    }

    if (swapRequestForm) {
        swapRequestForm.addEventListener("submit", handleSwapRequestSubmit);
    }

    if (deleteSkillBtn) {
        deleteSkillBtn.addEventListener("click", handleDeleteSkill);
    }

    document.querySelectorAll('[data-action="accept"]').forEach((btn) => {
        btn.addEventListener("click", handleAcceptRequest);
    });

    document.querySelectorAll('[data-action="reject"]').forEach((btn) => {
        btn.addEventListener("click", handleRejectRequest);
    });

    document.querySelectorAll('[data-action="cancel"]').forEach((btn) => {
        btn.addEventListener("click", handleCancelRequest);
    });

    function handleSkillFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const actionUrl = form.action || window.location.href;
        const isEdit = actionUrl.includes("/update/");

        Swal.fire({
            title: isEdit ? t("updateSkillTitle", "Update Skill?") : t("createSkillTitle", "Create Skill?"),
            text: isEdit
                ? t("updateSkillText", "Are you sure you want to update this skill?")
                : t("createSkillText", "Your new skill will be published."),
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#0d6efd",
            cancelButtonColor: "#6c757d",
            confirmButtonText: isEdit ? t("yesUpdate", "Yes, update it!") : t("yesCreate", "Yes, create it!"),
            cancelButtonText: t("cancel", "Cancel"),
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(actionUrl, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            Swal.fire({
                                title: t("success", "Success!"),
                                text: data.message,
                                icon: "success",
                                confirmButtonColor: "#198754",
                            }).then(() => {
                                if (data.redirect_url) {
                                    window.location.href = data.redirect_url;
                                }
                            });
                        } else {
                            Swal.fire({
                                title: t("error", "Error!"),
                                text: data.message,
                                icon: "error",
                                confirmButtonColor: "#dc3545",
                            });
                        }
                    })
                    .catch(() => {
                        Swal.fire({
                            title: t("error", "Error!"),
                            text: t("somethingWentWrong", "Something went wrong. Please try again."),
                            icon: "error",
                            confirmButtonColor: "#dc3545",
                        });
                    });
            }
        });
    }

    function handleSwapRequestSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const actionUrl = form.action || window.location.href;

        Swal.fire({
            title: t("sendRequestTitle", "Send Swap Request?"),
            text: t("sendRequestText", "Your request will be sent to the skill owner."),
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#198754",
            cancelButtonColor: "#6c757d",
            confirmButtonText: t("yesSend", "Yes, send it!"),
            cancelButtonText: t("cancel", "Cancel"),
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(actionUrl, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            Swal.fire({
                                title: t("success", "Success!"),
                                text: data.message,
                                icon: "success",
                                confirmButtonColor: "#198754",
                            }).then(() => {
                                if (data.redirect_url) {
                                    window.location.href = data.redirect_url;
                                }
                            });
                        } else {
                            Swal.fire({
                                title: t("error", "Error!"),
                                text: data.message,
                                icon: "error",
                                confirmButtonColor: "#dc3545",
                            });
                        }
                    })
                    .catch(() => {
                        Swal.fire({
                            title: t("error", "Error!"),
                            text: t("somethingWentWrong", "Something went wrong. Please try again."),
                            icon: "error",
                            confirmButtonColor: "#dc3545",
                        });
                    });
            }
        });
    }

    function handleDeleteSkill(e) {
        const btn = e.currentTarget;
        const form = document.getElementById("deleteSkillForm");

        if (!form) {
            console.error("Delete form not found");
            return;
        }

        Swal.fire({
            title: btn.dataset.swalTitle,
            text: btn.dataset.swalText,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#dc3545",
            cancelButtonColor: "#6c757d",
            confirmButtonText: btn.dataset.swalConfirm,
            cancelButtonText: btn.dataset.swalCancel,
        }).then((result) => {
            if (result.isConfirmed) {
                const formData = new FormData(form);

                fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                    .then((response) => {
                        return response.json();
                    })
                    .then((data) => {
                        if (data.success) {
                            Swal.fire({
                                title: (typeof translations !== "undefined" && translations.deleted) ? translations.deleted : "Deleted!",
                                text: data.message,
                                icon: "success",
                                confirmButtonColor: "#198754",
                            }).then(() => {
                                const redirectUrl = data.redirect_url || "/dashboard/skills/";
                                window.location.href = redirectUrl;
                            });
                        } else {
                            Swal.fire({
                                title: (typeof translations !== "undefined" && translations.error) ? translations.error : "Error!",
                                text: data.message,
                                icon: "error",
                                confirmButtonColor: "#dc3545",
                            });
                        }
                    })
                    .catch((error) => {
                        console.error("Fetch error:", error);
                        Swal.fire({
                            title: (typeof translations !== "undefined" && translations.error) ? translations.error : "Error!",
                            text: (typeof translations !== "undefined" && translations.somethingWentWrong) ? translations.somethingWentWrong : "Something went wrong. Please try again.",
                            icon: "error",
                            confirmButtonColor: "#dc3545",
                        });
                    });
            }
        });
    }

    function handleAcceptRequest(e) {
        const btn = e.currentTarget;
        const requestId = btn.dataset.requestId;

        Swal.fire({
            title: btn.dataset.swalTitle,
            text: btn.dataset.swalText,
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#198754",
            cancelButtonColor: "#6c757d",
            confirmButtonText: btn.dataset.swalConfirm,
            cancelButtonText: btn.dataset.swalCancel,
        }).then((result) => {
            if (result.isConfirmed) {
                const csrfTokenElement = document.querySelector(
                    '[name="csrfmiddlewaretoken"]'
                );
                const csrfToken = csrfTokenElement ? csrfTokenElement.value : getCookie("csrftoken");

                fetch(`/dashboard/swaps/${requestId}/accept/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            Swal.fire({
                                title: t("success", "Success!"),
                                text: data.message,
                                icon: "success",
                                confirmButtonColor: "#198754",
                            }).then(() => {
                                if (data.redirect_url) {
                                    window.location.href = data.redirect_url;
                                } else {
                                    location.reload();
                                }
                            });
                        } else {
                            Swal.fire({
                                title: t("error", "Error!"),
                                text: data.message,
                                icon: "error",
                                confirmButtonColor: "#dc3545",
                            });
                        }
                    })
                    .catch(() => {
                        Swal.fire({
                            title: t("error", "Error!"),
                            text: t("somethingWentWrong", "Something went wrong. Please try again."),
                            icon: "error",
                            confirmButtonColor: "#dc3545",
                        });
                    });
            }
        });
    }

    function handleRejectRequest(e) {
        const btn = e.currentTarget;
        const requestId = btn.dataset.requestId;

        Swal.fire({
            title: btn.dataset.swalTitle,
            text: btn.dataset.swalText,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#dc3545",
            cancelButtonColor: "#6c757d",
            confirmButtonText: btn.dataset.swalConfirm,
            cancelButtonText: btn.dataset.swalCancel,
        }).then((result) => {
            if (result.isConfirmed) {
                const csrfTokenElement = document.querySelector(
                    '[name="csrfmiddlewaretoken"]'
                );
                const csrfToken = csrfTokenElement ? csrfTokenElement.value : getCookie("csrftoken");

                fetch(`/dashboard/swaps/${requestId}/reject/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            Swal.fire({
                                title: t("rejected", "Rejected!"),
                                text: data.message,
                                icon: "success",
                                confirmButtonColor: "#198754",
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                title: t("error", "Error!"),
                                text: data.message,
                                icon: "error",
                                confirmButtonColor: "#dc3545",
                            });
                        }
                    })
                    .catch(() => {
                        Swal.fire({
                            title: t("error", "Error!"),
                            text: t("somethingWentWrong", "Something went wrong. Please try again."),
                            icon: "error",
                            confirmButtonColor: "#dc3545",
                        });
                    });
            }
        });
    }

    function handleCancelRequest(e) {
        const btn = e.currentTarget;
        const requestId = btn.dataset.requestId;

        Swal.fire({
            title: btn.dataset.swalTitle,
            text: btn.dataset.swalText,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#dc3545",
            cancelButtonColor: "#6c757d",
            confirmButtonText: btn.dataset.swalConfirm,
            cancelButtonText: btn.dataset.swalCancel,
        }).then((result) => {
            if (result.isConfirmed) {
                const csrfTokenElement = document.querySelector(
                    '[name="csrfmiddlewaretoken"]'
                );
                const csrfToken = csrfTokenElement ? csrfTokenElement.value : getCookie("csrftoken");

                fetch(`/dashboard/swaps/${requestId}/cancel/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            Swal.fire({
                                title: t("cancelled", "Cancelled!"),
                                text: data.message,
                                icon: "success",
                                confirmButtonColor: "#198754",
                            }).then(() => {
                                if (data.redirect_url) {
                                    window.location.href = data.redirect_url;
                                } else {
                                    location.reload();
                                }
                            });
                        } else {
                            Swal.fire({
                                title: t("error", "Error!"),
                                text: data.message,
                                icon: "error",
                                confirmButtonColor: "#dc3545",
                            });
                        }
                    })
                    .catch(() => {
                        Swal.fire({
                            title: t("error", "Error!"),
                            text: t("somethingWentWrong", "Something went wrong. Please try again."),
                            icon: "error",
                            confirmButtonColor: "#dc3545",
                        });
                    });
            }
        });
    }

});
