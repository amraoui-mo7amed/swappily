from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

from dashboard.models import Skill, SwapRequest
from dashboard.utils import notify_user


@login_required
def skill_list(request):
    query = request.GET.get("q", "")
    skills_list = Skill.objects.select_related("user").all().order_by("-created_at")

    if query:
        skills_list = skills_list.filter(
            Q(skill_title__icontains=query) | Q(skill_description__icontains=query)
        )

    paginator = Paginator(skills_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "skills": page_obj,
        "query": query,
    }

    return render(request, "skills/list.html", context)


@login_required
def skill_detail(request, pk):
    skill = get_object_or_404(Skill.objects.select_related("user"), pk=pk)
    user_skills = Skill.objects.filter(user=request.user).exclude(pk=skill.pk)

    pending_request = None
    if request.user != skill.user:
        pending_request = (
            SwapRequest.objects.select_related(
                "requester", "target_skill", "offered_skill"
            )
            .filter(
                requester=request.user,
                target_skill=skill,
                status=SwapRequest.StatusChoices.PENDING,
            )
            .first()
        )

    context = {
        "skill": skill,
        "user_skills": user_skills,
        "pending_request": pending_request,
        "is_owner": request.user == skill.user,
    }

    return render(request, "skills/detail.html", context)


@login_required
def skill_create(request):
    if request.method == "POST":
        skill_title = request.POST.get("skill_title")
        skill_description = request.POST.get("skill_description")
        skill_image = request.FILES.get("skill_image")

        if not skill_title or not skill_description:
            return JsonResponse(
                {"success": False, "message": _("Title and description are required.")}
            )

        skill = Skill.objects.create(
            user=request.user,
            skill_title=skill_title,
            skill_description=skill_description,
            skill_image=skill_image if skill_image else None,
        )

        return JsonResponse(
            {
                "success": True,
                "message": _("Skill created successfully!"),
                "redirect_url": reverse("dash:skill_detail", args=[skill.pk]),
            }
        )

    return render(request, "skills/form.html")


@login_required
def skill_update(request, pk):
    skill = get_object_or_404(Skill, pk=pk)

    if request.user != skill.user:
        return JsonResponse(
            {"success": False, "message": _("You can only edit your own skills.")},
            status=403,
        )

    if request.method == "POST":
        skill_title = request.POST.get("skill_title")
        skill_description = request.POST.get("skill_description")
        skill_image = request.FILES.get("skill_image")

        if not skill_title or not skill_description:
            return JsonResponse(
                {"success": False, "message": _("Title and description are required.")}
            )

        skill.skill_title = skill_title
        skill.skill_description = skill_description
        if skill_image:
            skill.skill_image = skill_image
        skill.save()

        return JsonResponse(
            {
                "success": True,
                "message": _("Skill updated successfully!"),
                "redirect_url": reverse("dash:skill_detail", args=[skill.pk]),
            }
        )

    return render(request, "skills/form.html", {"skill": skill})


@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)

    if request.user != skill.user:
        return JsonResponse(
            {"success": False, "message": _("You can only delete your own skills.")},
            status=403,
        )

    if request.method == "POST":
        skill_title = skill.skill_title
        skill.delete()

        return JsonResponse(
            {
                "success": True,
                "message": _("Skill '%(title)s' deleted successfully.")
                % {"title": skill_title},
                "redirect_url": reverse("dash:skill_list"),
            }
        )

    return redirect("dash:skill_detail", pk=pk)


@login_required
def swap_request_create(request, pk):
    target_skill = get_object_or_404(Skill, pk=pk)

    if request.user == target_skill.user:
        return JsonResponse(
            {"success": False, "message": _("You cannot swap your own skill.")},
            status=400,
        )

    existing_request = SwapRequest.objects.filter(
        requester=request.user,
        target_skill=target_skill,
        status=SwapRequest.StatusChoices.PENDING,
    ).exists()

    if existing_request:
        return JsonResponse(
            {
                "success": False,
                "message": _("You already have a pending request for this skill."),
            },
            status=400,
        )

    if request.method == "POST":
        offered_skill_id = request.POST.get("offered_skill")
        message = request.POST.get("message", "")
        requester_pdf = request.FILES.get("requester_pdf")
        requester_video = request.FILES.get("requester_video")

        if not offered_skill_id:
            return JsonResponse(
                {"success": False, "message": _("Please select a skill to offer.")},
                status=400,
            )

        try:
            offered_skill = Skill.objects.get(pk=offered_skill_id, user=request.user)
        except Skill.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": _("Invalid skill selected.")}, status=400
            )

        with transaction.atomic():
            swap_request = SwapRequest.objects.create(
                requester=request.user,
                target_skill=target_skill,
                offered_skill=offered_skill,
                message=message,
                requester_pdf=requester_pdf if requester_pdf else None,
                requester_video=requester_video if requester_video else None,
            )

            notify_user(
                user=target_skill.user,
                title=_("New Swap Request"),
                message=_(
                    "%(username)s wants to swap their '%(offered)s' for your '%(target)s'"
                )
                % {
                    "username": request.user.username,
                    "offered": offered_skill.skill_title,
                    "target": target_skill.skill_title,
                },
                notification_type="info",
                link=reverse("dash:swap_request_detail", args=[swap_request.pk]),
            )

        return JsonResponse(
            {
                "success": True,
                "message": _("Swap request sent successfully!"),
                "redirect_url": reverse("dash:skill_detail", args=[target_skill.pk]),
            }
        )

    user_skills = Skill.objects.filter(user=request.user).exclude(pk=target_skill.pk)
    user_skill_choices = [(s.pk, s.skill_title) for s in user_skills]

    context = {
        "target_skill": target_skill,
        "user_skills": user_skills,
        "user_skill_choices": user_skill_choices,
    }

    return render(request, "skills/swap_request_form.html", context)


@login_required
def swap_request_list(request):
    received_requests = SwapRequest.objects.filter(
        target_skill__user=request.user
    ).select_related(
        "requester",
        "target_skill__user",
        "offered_skill__user",
    )

    sent_requests = SwapRequest.objects.filter(requester=request.user).select_related(
        "target_skill__user",
        "offered_skill__user",
    )

    received_paginator = Paginator(received_requests, 10)
    received_page = request.GET.get("received_page")
    received_page_obj = received_paginator.get_page(received_page)

    sent_paginator = Paginator(sent_requests, 10)
    sent_page = request.GET.get("sent_page")
    sent_page_obj = sent_paginator.get_page(sent_page)

    context = {
        "received_requests": received_page_obj,
        "sent_requests": sent_page_obj,
    }

    return render(request, "skills/swap_requests.html", context)


@login_required
def swap_request_detail(request, pk):
    swap_request = get_object_or_404(
        SwapRequest.objects.select_related(
            "requester",
            "target_skill__user",
            "offered_skill__user",
        ),
        pk=pk,
    )

    is_recipient = request.user == swap_request.target_skill.user
    is_requester = request.user == swap_request.requester

    if not is_recipient and not is_requester:
        return redirect("dash:swap_request_list")

    context = {
        "swap_request": swap_request,
        "is_recipient": is_recipient,
        "is_requester": is_requester,
    }

    return render(request, "skills/swap_request_detail.html", context)


@login_required
def swap_request_accept_form(request, pk):
    swap_request = get_object_or_404(
        SwapRequest.objects.select_related(
            "requester",
            "target_skill__user",
            "offered_skill__user",
        ),
        pk=pk,
    )

    if request.user != swap_request.target_skill.user:
        return redirect("dash:swap_request_list")

    if swap_request.status != SwapRequest.StatusChoices.PENDING:
        return redirect("dash:swap_request_detail", pk=pk)

    return render(
        request, "skills/swap_accept_form.html", {"swap_request": swap_request}
    )


@login_required
def swap_request_accept(request, pk):
    swap_request = get_object_or_404(
        SwapRequest.objects.select_related(
            "requester",
            "target_skill__user",
            "offered_skill__user",
        ),
        pk=pk,
    )

    if request.user != swap_request.target_skill.user:
        return JsonResponse(
            {
                "success": False,
                "message": _("Only the skill owner can accept requests."),
            },
            status=403,
        )

    if request.method == "POST":
        owner_pdf = request.FILES.get("owner_pdf")
        owner_video = request.FILES.get("owner_video")

        if swap_request.accept():
            if owner_pdf:
                swap_request.owner_pdf = owner_pdf
            if owner_video:
                swap_request.owner_video = owner_video
            swap_request.save()

            notify_user(
                user=swap_request.requester,
                title=_("Swap Request Accepted"),
                message=_(
                    "Your swap request for '%(skill)s' has been accepted by %(owner)s!"
                )
                % {
                    "skill": swap_request.target_skill.skill_title,
                    "owner": request.user.username,
                },
                notification_type="success",
                link=reverse("dash:swap_request_detail", args=[swap_request.pk]),
            )

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": True,
                        "message": _("Swap request accepted successfully!"),
                        "redirect_url": reverse(
                            "dash:swap_request_detail", args=[swap_request.pk]
                        ),
                    }
                )
            return redirect("dash:swap_request_detail", pk=pk)
        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("This request cannot be accepted."),
                    },
                    status=400,
                )
            return redirect("dash:swap_request_detail", pk=pk)

    return redirect("dash:swap_request_detail", pk=pk)


@login_required
def swap_request_reject(request, pk):
    swap_request = get_object_or_404(
        SwapRequest.objects.select_related(
            "requester",
            "target_skill__user",
            "offered_skill__user",
        ),
        pk=pk,
    )

    if request.user != swap_request.target_skill.user:
        return JsonResponse(
            {
                "success": False,
                "message": _("Only the skill owner can reject requests."),
            },
            status=403,
        )

    if request.method == "POST":
        if swap_request.reject():
            notify_user(
                user=swap_request.requester,
                title=_("Swap Request Rejected"),
                message=_(
                    "Your swap request for '%(skill)s' has been rejected by %(owner)s."
                )
                % {
                    "skill": swap_request.target_skill.skill_title,
                    "owner": request.user.username,
                },
                notification_type="warning",
                link=reverse("dash:swap_request_detail", args=[swap_request.pk]),
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": _("Swap request rejected."),
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": _("This request cannot be rejected.")},
                status=400,
            )

    return redirect("dash:swap_request_detail", pk=pk)


@login_required
def swap_request_cancel(request, pk):
    swap_request = get_object_or_404(
        SwapRequest.objects.select_related(
            "requester",
            "target_skill__user",
            "offered_skill__user",
        ),
        pk=pk,
    )

    if request.user != swap_request.requester:
        return JsonResponse(
            {"success": False, "message": _("You can only cancel your own requests.")},
            status=403,
        )

    if request.method == "POST":
        if swap_request.status == SwapRequest.StatusChoices.PENDING:
            swap_request.delete()
            return JsonResponse(
                {
                    "success": True,
                    "message": _("Swap request cancelled successfully!"),
                    "redirect_url": reverse("dash:swap_request_list"),
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": _("This request cannot be cancelled.")},
                status=400,
            )

    return redirect("dash:swap_request_detail", pk=pk)
