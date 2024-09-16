import requests
from app.core.config import settings



def authiiko():
    data = requests.get(
        f"{settings.base_url}/resto/api/auth?login={settings.login_iiko}&pass={settings.password_iiko}"
    )

    key = data.text
    return key

def send_inventory_document_iiko(key, data):
    if data.tool.price:
        total_price = float(data.amount) * float(data.tool.price)
        price = data.tool.price

    else:
        total_price = 0
        price = 0


    headers = {
        "Content-Type": "application/xml",  # Set the content type to XML
    }
    xml_data = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <document>
        <documentNumber>newinv-{data.id}</documentNumber>
        <dateIncoming></dateIncoming>
        <useDefaultDocumentTime>false</useDefaultDocumentTime>
        <counteragentId>{data.request.fillial.supplier[0].id}</counteragentId>
        <defaultStoreId>0bfe01f2-6864-48f5-a79e-c885dc76116a</defaultStoreId>
        <items>
            <item>
                <productId>{data.tool.iikoid}</productId>
                <productArticle>{data.tool.code}</productArticle>
                <storeId>0bfe01f2-6864-48f5-a79e-c885dc76116a</storeId>
                <price>{price}</price>
                <amount>{data.amount}</amount>
                <sum>{total_price}</sum>
                <discountSum>0.000000000</discountSum>
            </item>
        </items>
        </document>"""

    response = requests.post(
        f"{settings.base_url}/resto/api/documents/import/outgoingInvoice?key={key}",
        data=xml_data,
        headers=headers,
    )
    return True



def send_arc_document_iiko(key, data):
    if data.tool.price:
        total_price = float(data.amount) * float(data.tool.price)
        price = data.tool.price

    else:
        total_price = 0
        price = 0
    headers = {
        "Content-Type": "application/xml",  # Set the content type to XML
    }
    xml_data = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <document>
                    <documentNumber>newarc-{data.id}</documentNumber>
                    <dateIncoming></dateIncoming>
                    <useDefaultDocumentTime>false</useDefaultDocumentTime>
                    <counteragentId>{data.request.fillial.supplier[0].id}</counteragentId>
                    <defaultStoreId>4aafb5af-66c3-4419-af2d-72897f652019</defaultStoreId>
                    <items>
                        <item>
                            <productId>{data.tool.iikoid}</productId>
                            <productArticle>{data.tool.code}</productArticle>
                            <storeId>4aafb5af-66c3-4419-af2d-72897f652019</storeId>
                            <price>{price}</price>
                            <amount>{data.amount}</amount>
                            <sum>{total_price}</sum>
                            <discountSum>0.000000000</discountSum>
                        </item>
                    </items>
                    </document>"""

    response = requests.post(
        f"{settings.base_url}/resto/api/documents/import/outgoingInvoice?key={key}",
        data=xml_data,
        headers=headers,
    )
    return True

