from azure.communication.email import EmailClient #pip install azure-communication-email==1.0.0 & https://pypi.org/project/azure-communication-email/1.0.0/
# https://azure.github.io/azure-sdk/releases/latest/all/python.html للمزيد من المعلومات
# https://portal.azure.com/ للحصول على accesskey & endpoint
# https://www.youtube.com/watch?v=m1XjECB2ZxY
# https://pypi.org/project/azure/ هذه المكتبة انتهت صلاحيته ولاكن فيه معلومات عن المكاتب الجديدة
connection_string = "endpoint=https://qad-email.unitedstates.communication.azure.com/;accesskey=xb+NBF/P+SVfr6IUBvCwr7T4dTeTY3rtBpA0NNoKAsNkUpXnEw2M+CJe+8ITIZXZkcziqrsztC3AncY05Y5b+Q=="
client = EmailClient.from_connection_string(connection_string);



message = {
    "content": {
        "subject": "This is the subject",
        "plainText": "This is the body",
        "html": "html><h1>This is the body</h1></html>"
    },
    "recipients": {
        "to": [
            {
                "address": "customer@domain.com",
                "displayName": "Customer Name"
            }
        ]
    },
    "senderAddress": "sender@contoso.com"
}

poller = client.begin_send(message)
result = poller.result()