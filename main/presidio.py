from presidio_analyzer import AnalyzerEngine 
from presidio_anonymizer import AnonymizerEngine 

analyzer = AnalyzerEngine() 
anonymizer = AnonymizerEngine() 

entity_names = [
    "CREDIT_CARD",
    "CRYPTO",
    "EMAIL_ADDRESS",
    "IBAN_CODE",
    "IP_ADDRESS",
    # "PERSON",
    "PHONE_NUMBER",
    "MEDICAL_LICENSE",
    "URL",
    "USA",
    "US_BANK_NUMBER",
    "US_DRIVER_LICENSE",
    "US_ITIN",
    "US_PASSPORT",
    "US_SSN",
    "UK",
    "UK_NHS",
    "Spain",
    "ES_NIF",
    "Italy",
    "IT_FISCAL_CODE",
    "IT_DRIVER_LICENSE",
    "IT_VAT_CODE",
    "IT_PASSPORT",
    "IT_IDENTITY_CARD"
]

def anonymize(query):
    analyze = analyzer.analyze(query, language="en",  entities=entity_names) 
    results = anonymizer.anonymize(text=query, analyzer_results=analyze).text
    return results