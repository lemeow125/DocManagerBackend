from djoser import email
from config.settings import FRONTEND_URL


class RequestUpdateEmail(email.BaseEmailMessage):
    template_name = "request_approved.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["request_status"] = context.get("request_status")
        context["url"] = FRONTEND_URL
        context.update(self.context)
        return context
