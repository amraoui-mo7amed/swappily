from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

userModel = get_user_model()


class Skill(models.Model):
    """Skill model for skill exchanging system"""

    user = models.ForeignKey(
        userModel,
        on_delete=models.CASCADE,
        related_name="skills",
        verbose_name=_("user"),
    )
    skill_title = models.CharField(
        max_length=200,
        verbose_name=_("skill title"),
    )
    skill_description = models.TextField(
        verbose_name=_("skill description"),
    )
    skill_image = models.ImageField(
        upload_to="skills",
        verbose_name=_("skill image"),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاريخ الإنشاء")
    )

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.skill_title} - {self.user.username}"


class Notification(models.Model):
    """Notification model for user notifications"""

    class NotificationType(models.TextChoices):
        INFO = "info", _("معلومة")
        SUCCESS = "success", _("نجاح")
        WARNING = "warning", _("تحذير")
        ERROR = "error", _("خطأ")

    user = models.ForeignKey(
        userModel,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("المستخدم"),
    )
    title = models.CharField(max_length=255, verbose_name=_("العنوان"))
    message = models.TextField(verbose_name=_("الرسالة"))
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
        verbose_name=_("نوع الإشعار"),
    )
    is_read = models.BooleanField(default=False, verbose_name=_("مقروء"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاريخ الإنشاء")
    )
    read_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("تاريخ القراءة")
    )
    link = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("الرابط"),
        help_text=_("رابط اختياري للتنقل"),
    )

    class Meta:
        verbose_name = _("إشعار")
        verbose_name_plural = "الإشعارات"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class SwapRequest(models.Model):
    """Swap request model for skill exchanging"""

    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACCEPTED = "accepted", _("Accepted")
        REJECTED = "rejected", _("Rejected")

    requester = models.ForeignKey(
        userModel,
        on_delete=models.CASCADE,
        related_name="sent_swap_requests",
        verbose_name=_("requester"),
    )
    target_skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="swap_requests",
        verbose_name=_("target skill"),
    )
    offered_skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="offered_in_requests",
        verbose_name=_("offered skill"),
    )
    message = models.TextField(
        blank=True,
        verbose_name=_("message"),
        help_text=_("Optional message to the skill owner"),
    )
    requester_pdf = models.FileField(
        upload_to="swap_requests/requester",
        blank=True,
        null=True,
        verbose_name=_("requester PDF"),
        help_text=_("PDF file from requester"),
    )
    requester_video = models.FileField(
        upload_to="swap_requests/requester",
        blank=True,
        null=True,
        verbose_name=_("requester video"),
        help_text=_("Video file from requester"),
    )
    owner_pdf = models.FileField(
        upload_to="swap_requests/owner",
        blank=True,
        null=True,
        verbose_name=_("owner PDF"),
        help_text=_("PDF file from skill owner"),
    )
    owner_video = models.FileField(
        upload_to="swap_requests/owner",
        blank=True,
        null=True,
        verbose_name=_("owner video"),
        help_text=_("Video file from skill owner"),
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_("status"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاريخ الإنشاء")
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاريخ التحديث"))

    class Meta:
        verbose_name = _("Swap Request")
        verbose_name_plural = _("Swap Requests")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.requester.username} wants to swap {self.offered_skill.skill_title} for {self.target_skill.skill_title}"

    def accept(self):
        """Accept the swap request"""
        if self.status == self.StatusChoices.PENDING:
            self.status = self.StatusChoices.ACCEPTED
            self.save(update_fields=["status", "updated_at"])
            return True
        return False

    def reject(self):
        """Reject the swap request"""
        if self.status == self.StatusChoices.PENDING:
            self.status = self.StatusChoices.REJECTED
            self.save(update_fields=["status", "updated_at"])
            return True
        return False
