
import json
import os
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"

LANGUAGE_NAMES = {
    "Telugu": "Telugu", "te-IN": "Telugu",
    "Hindi": "Hindi", "hi-IN": "Hindi",
    "English": "English", "en-IN": "English",
    "Tamil": "Tamil", "ta-IN": "Tamil",
}

LOCALIZED = {
    "PM-KISAN Samman Nidhi": {
        "Telugu": "PM-KISAN అనేది అర్హత కలిగిన భూమి కలిగిన రైతు కుటుంబాలకు ఆదాయ సహాయం అందించే కేంద్ర ప్రభుత్వ పథకం. అర్హతకు నియమాలు మరియు మినహాయింపులు ఉంటాయి. భూమి ఉందని మాత్రమే అర్హత నిర్ధారించలేం. నమోదు, e-KYC మరియు లబ్ధిదారుల స్థితిని అధికారిక పోర్టల్‌లో తనిఖీ చేయండి.",
        "Hindi": "PM-KISAN पात्र भूमिधारक किसान परिवारों को आय सहायता देने वाली केंद्र सरकार की योजना है। पात्रता नियम और अपवाद लागू होते हैं। केवल जमीन होने से पात्रता निश्चित नहीं होती। पंजीकरण, e-KYC और लाभार्थी स्थिति आधिकारिक पोर्टल पर जांचें।",
        "Tamil": "PM-KISAN என்பது தகுதியுள்ள நிலம் வைத்திருக்கும் விவசாயக் குடும்பங்களுக்கு வருமான ஆதரவு வழங்கும் மத்திய அரசுத் திட்டமாகும். தகுதி விதிமுறைகளும் விலக்குகளும் உள்ளன. நிலம் இருப்பதால் மட்டும் தகுதி உறுதி ஆகாது. பதிவு, e-KYC மற்றும் பயனாளர் நிலையை அதிகாரப்பூர்வ இணையதளத்தில் சரிபார்க்கவும்.",
    },
    "Pradhan Mantri Fasal Bima Yojana (PMFBY)": {
        "Telugu": "PMFBY పంట బీమా పథకం. ఏ పంటలు, ప్రాంతాలు అర్హం, నమోదు గడువు, ప్రీమియం మరియు క్లెయిమ్ నియమాలు సీజన్ మరియు రాష్ట్ర ప్రకటనపై ఆధారపడి ఉంటాయి. ప్రస్తుత వివరాలను అధికారిక పోర్టల్ లేదా జిల్లా వ్యవసాయ కార్యాలయంలో నిర్ధారించండి.",
        "Hindi": "PMFBY एक फसल बीमा योजना है। फसल, क्षेत्र, आवेदन अवधि, प्रीमियम और दावा नियम मौसम तथा राज्य की अधिसूचना पर निर्भर करते हैं। वर्तमान जानकारी आधिकारिक पोर्टल या जिला कृषि कार्यालय से जांचें।",
        "Tamil": "PMFBY ஒரு பயிர் காப்பீட்டுத் திட்டமாகும். பயிர், பகுதி, பதிவு காலம், பிரீமியம் மற்றும் இழப்பீட்டு விதிகள் பருவம் மற்றும் மாநில அறிவிப்பைப் பொறுத்தது. தற்போதைய விவரங்களை அதிகாரப்பூர்வ இணையதளம் அல்லது மாவட்ட வேளாண்மை அலுவலகத்தில் சரிபார்க்கவும்.",
    },
    "Kisan Credit Card (KCC)": {
        "Telugu": "Kisan Credit Card (KCC) రైతుల వ్యవసాయ మరియు అనుబంధ అవసరాలకు బ్యాంకు రుణ సదుపాయం. అర్హత, రుణ పరిమితి, వడ్డీ ప్రయోజనాలు మరియు పత్రాలను సంబంధిత బ్యాంకు ప్రస్తుత నియమాల ప్రకారం నిర్ణయిస్తుంది.",
        "Hindi": "किसान क्रेडिट कार्ड (KCC) किसानों की कृषि और उससे जुड़ी जरूरतों के लिए बैंक ऋण सुविधा है। पात्रता, ऋण सीमा, ब्याज लाभ और दस्तावेज संबंधित बैंक के मौजूदा नियमों के अनुसार तय होते हैं।",
        "Tamil": "கிசான் கிரெடிட் கார்டு (KCC) விவசாயம் மற்றும் அதனுடன் தொடர்புடைய தேவைகளுக்கான வங்கிக் கடன் வசதியாகும். தகுதி, கடன் வரம்பு, வட்டி சலுகைகள் மற்றும் ஆவணங்களை சம்பந்தப்பட்ட வங்கி தற்போதைய விதிகளின்படி தீர்மானிக்கும்.",
    },
    "PM-KUSUM": {
        "Telugu": "PM-KUSUM వ్యవసాయంలో సౌర పంపులు మరియు సౌర విద్యుత్ వినియోగానికి సంబంధించిన భాగాలకు మద్దతు ఇస్తుంది. ఏ భాగం అందుబాటులో ఉంది, రైతు వాటా మరియు దరఖాస్తు విధానం రాష్ట్ర అమలు మరియు ప్రస్తుత దరఖాస్తులపై ఆధారపడి ఉంటాయి.",
        "Hindi": "PM-KUSUM कृषि में सौर पंप और सौर ऊर्जा से जुड़ी योजनाओं को सहायता देती है। उपलब्ध घटक, किसान का अंशदान और आवेदन प्रक्रिया राज्य के नियमों तथा वर्तमान आवेदन अवधि पर निर्भर करते हैं।",
        "Tamil": "PM-KUSUM விவசாயத்தில் சூரிய மின்சார பம்புகள் மற்றும் சூரிய ஆற்றல் பயன்பாட்டுக்கான திட்டங்களுக்கு ஆதரவு அளிக்கிறது. கிடைக்கும் பகுதி, விவசாயியின் பங்களிப்பு மற்றும் விண்ணப்ப முறை மாநில செயல்பாடு மற்றும் தற்போதைய விண்ணப்ப காலத்தைப் பொறுத்தது.",
    },
    "Telangana Rythu Bharosa": {
        "Telugu": "రైతు భరోసా తెలంగాణ ప్రభుత్వ వ్యవసాయ పెట్టుబడి సహాయ కార్యక్రమం. రైతు బంధు అనే పాత పేరుతో కూడా ప్రజలు అడగవచ్చు. ప్రస్తుత అర్హత, సహాయం మొత్తం, భూమి లేదా సాగు షరతులు మరియు చెల్లింపు వివరాలను తాజా ప్రభుత్వ ఉత్తర్వులు, అధికారిక పోర్టల్‌లో నిర్ధారించండి.",
        "Hindi": "रायथु भरोसा तेलंगाना सरकार की कृषि निवेश सहायता योजना है। लोग इसे पुराने नाम रायथु बंधु से भी पूछ सकते हैं। वर्तमान पात्रता, सहायता राशि, भूमि या खेती की शर्तें और भुगतान विवरण नवीनतम सरकारी आदेशों तथा आधिकारिक पोर्टल से जांचें।",
        "Tamil": "ரைது பரோசா தெலங்கானா அரசின் விவசாய முதலீட்டு உதவித் திட்டமாகும். சிலர் இதை பழைய பெயரான ரைது பந்து என்றும் கேட்கலாம். தற்போதைய தகுதி, உதவித் தொகை, நிலம் அல்லது சாகுபடி நிபந்தனைகள் மற்றும் கட்டண விவரங்களை சமீபத்திய அரசு உத்தரவுகள் மற்றும் அதிகாரப்பூர்வ தளத்தில் சரிபார்க்கவும்.",
    },
    "Telangana Crop Loan Waiver": {
        "Telugu": "తెలంగాణ పంట రుణ మాఫీ పథకం నిర్దిష్ట నిబంధనలకు లోబడి అర్హత కలిగిన పంట రుణాలకు వర్తిస్తుంది. రుణ తేదీలు, రైతు వివరాలు, పరిమితులు మరియు స్థితిని అధికారిక పోర్టల్‌లో తాజా మార్గదర్శకాల ప్రకారం తనిఖీ చేయండి.",
        "Hindi": "तेलंगाना फसल ऋण माफी योजना निर्धारित नियमों के तहत पात्र फसल ऋणों पर लागू होती है। ऋण की तारीख, किसान की जानकारी, सीमा और स्थिति नवीनतम निर्देशों के अनुसार आधिकारिक पोर्टल पर जांचें।",
        "Tamil": "தெலங்கானா பயிர் கடன் தள்ளுபடி திட்டம் குறிப்பிட்ட விதிகளின் கீழ் தகுதியுள்ள பயிர் கடன்களுக்கு பொருந்தும். கடன் தேதி, விவசாயி விவரங்கள், வரம்பு மற்றும் நிலையை அதிகாரப்பூர்வ தளத்தில் சரிபார்க்கவும்.",
    },
    "Telangana Aarogyasri": {
        "Telugu": "ఆరోగ్యశ్రీ తెలంగాణలో అర్హత కలిగిన కుటుంబాలకు ఎంపిక చేసిన చికిత్సల కోసం ఆరోగ్య రక్షణ అందిస్తుంది. చికిత్స, ఆసుపత్రి, అర్హత మరియు కవరేజ్ వివరాలను అధికారిక ఆరోగ్యశ్రీ వేదిక లేదా ఆసుపత్రి సహాయ కేంద్రంలో నిర్ధారించండి.",
        "Hindi": "आरोग्यश्री तेलंगाना में पात्र परिवारों को निर्धारित उपचारों के लिए स्वास्थ्य सुरक्षा देती है। उपचार, अस्पताल, पात्रता और कवरेज की पुष्टि आधिकारिक पोर्टल या अस्पताल सहायता केंद्र से करें।",
        "Tamil": "ஆரோக்கியஸ்ரீ தெலங்கானாவில் தகுதியுள்ள குடும்பங்களுக்கு அறிவிக்கப்பட்ட சிகிச்சைகளுக்கான சுகாதார பாதுகாப்பை வழங்குகிறது. சிகிச்சை, மருத்துவமனை, தகுதி மற்றும் காப்பீட்டு விவரங்களை அதிகாரப்பூர்வ தளம் அல்லது மருத்துவமனை உதவி மையத்தில் உறுதிப்படுத்தவும்.",
    },
    "Telangana ePASS Scholarships": {
        "Telugu": "తెలంగాణ ePASS ద్వారా అర్హత కలిగిన విద్యార్థులు స్కాలర్‌షిప్ మరియు ఫీజు రీయింబర్స్‌మెంట్ సేవలకు దరఖాస్తు చేయవచ్చు. కోర్సు, వర్గం, ఆదాయం, హాజరు మరియు పత్రాల నియమాలు పథకం మరియు విద్యా సంవత్సరాన్ని బట్టి మారుతాయి.",
        "Hindi": "तेलंगाना ePASS के माध्यम से पात्र विद्यार्थी छात्रवृत्ति और फीस प्रतिपूर्ति के लिए आवेदन कर सकते हैं। पाठ्यक्रम, श्रेणी, आय, उपस्थिति और दस्तावेजों की शर्तें योजना तथा शैक्षणिक वर्ष के अनुसार बदलती हैं।",
        "Tamil": "தெலங்கானா ePASS மூலம் தகுதியுள்ள மாணவர்கள் கல்வி உதவித்தொகை மற்றும் கட்டணத் திருப்பிச் செலுத்தலுக்கு விண்ணப்பிக்கலாம். பாடநெறி, பிரிவு, வருமானம், வருகை மற்றும் ஆவண விதிகள் திட்டம் மற்றும் கல்வியாண்டைப் பொறுத்து மாறும்.",
    },
    "Telangana Gruha Jyothi": {
        "Telugu": "గ్రుహ జ్యోతి అర్హత కలిగిన తెలంగాణ గృహ విద్యుత్ వినియోగదారులకు బిల్లు రాయితీకి సంబంధించిన కార్యక్రమం. అర్హత, వినియోగ పరిమితి మరియు కనెక్షన్ నియమాలను విద్యుత్ పంపిణీ సంస్థ లేదా తాజా ప్రభుత్వ ప్రకటనలో నిర్ధారించండి.",
        "Hindi": "गृह ज्योति तेलंगाना के पात्र घरेलू बिजली उपभोक्ताओं के लिए बिल राहत से जुड़ी योजना है। पात्रता, खपत सीमा और कनेक्शन नियम बिजली वितरण कंपनी या नवीनतम सरकारी सूचना से जांचें।",
        "Tamil": "கிருஹ ஜ்யோதி தெலங்கானாவின் தகுதியுள்ள வீட்டு மின்சார நுகர்வோருக்கான கட்டண நிவாரணத் திட்டம். தகுதி, பயன்பாட்டு வரம்பு மற்றும் இணைப்பு விதிகளை மின்விநியோக நிறுவனம் அல்லது சமீபத்திய அரசு அறிவிப்பில் சரிபார்க்கவும்.",
    },
    "Telangana Aasara Pensions": {
        "Telugu": "ఆసరా తెలంగాణ ప్రభుత్వ సామాజిక భద్రతా పెన్షన్ కార్యక్రమం. వయస్సు, వర్గం, ఆదాయం మరియు ఇతర అర్హతలు తాజా రాష్ట్ర నిబంధనల ప్రకారం మారవచ్చు. స్థానిక గ్రామపంచాయతీ, మున్సిపాలిటీ లేదా సంక్షేమ కార్యాలయంలో నిర్ధారించండి.",
        "Hindi": "आसरा तेलंगाना की सामाजिक सुरक्षा पेंशन योजना है। आयु, श्रेणी, आय और अन्य पात्रता शर्तें वर्तमान राज्य नियमों के अनुसार बदल सकती हैं। स्थानीय पंचायत, नगरपालिका या कल्याण कार्यालय से पुष्टि करें।",
        "Tamil": "ஆசரா தெலங்கானா அரசின் சமூக பாதுகாப்பு ஓய்வூதியத் திட்டம். வயது, பிரிவு, வருமானம் மற்றும் பிற தகுதி நிபந்தனைகள் தற்போதைய மாநில விதிகளின்படி மாறலாம். உள்ளூர் ஊராட்சி, நகராட்சி அல்லது நலத்துறை அலுவலகத்தில் உறுதிப்படுத்தவும்.",
    },
    "Telangana Maha Lakshmi": {
        "Telugu": "మహాలక్ష్మి తెలంగాణ ప్రభుత్వ కార్యక్రమం. ఇందులోని ప్రయోజనాల అర్హత, సేవా షరతులు మరియు అమలు విధానం తాజా అధికారిక ప్రకటనల ప్రకారం నిర్ధారించాలి.",
        "Hindi": "महालक्ष्मी तेलंगाना सरकार की पहल है। इसके लाभों की पात्रता, सेवा शर्तें और लागू प्रक्रिया नवीनतम आधिकारिक सूचनाओं से जांचें।",
        "Tamil": "மகாலட்சுமி தெலங்கானா அரசின் திட்டமாகும். இதன் நன்மைகளுக்கான தகுதி, சேவை நிபந்தனைகள் மற்றும் நடைமுறையை சமீபத்திய அதிகாரப்பூர்வ அறிவிப்புகளில் சரிபார்க்கவும்.",
    },
    "Telangana Kalyana Lakshmi / Shaadi Mubarak": {
        "Telugu": "కళ్యాణ లక్ష్మి మరియు షాదీ ముబారక్ పథకాలు తెలంగాణలో నిర్దిష్ట వర్గాలకు వివాహ సహాయం అందించే సంక్షేమ పథకాలు. వయస్సు, ఆదాయం, నివాసం, వివాహ తేదీ మరియు అవసరమైన పత్రాలను ప్రస్తుత అధికారిక నిబంధనల ప్రకారం తనిఖీ చేయండి.",
        "Hindi": "कल्याण लक्ष्मी और शादी मुबारक तेलंगाना में निर्धारित श्रेणियों के लिए विवाह सहायता योजनाएं हैं। आयु, आय, निवास, विवाह की तारीख और दस्तावेज वर्तमान आधिकारिक नियमों से जांचें।",
        "Tamil": "கல்யாண லட்சுமி மற்றும் ஷாதி முபாரக் தெலங்கானாவில் குறிப்பிட்ட பிரிவினருக்கான திருமண உதவித் திட்டங்கள். வயது, வருமானம், வசிப்பிடம், திருமண தேதி மற்றும் ஆவணங்களை தற்போதைய அதிகாரப்பூர்வ விதிகளின்படி சரிபார்க்கவும்.",
    },
}

GENERAL_TEXT = {
    "Telugu": "క్షమించండి, ఈ ప్రశ్నకు సరిపడే ధృవీకరించిన సమాచారం ప్రస్తుతం నా సమాచార గ్రంథాలయంలో లేదు. పథకం పేరు, జిల్లా లేదా సంబంధిత శాఖ వివరాలు చెప్పండి. ఊహించి అర్హతలు లేదా గడువులు చెప్పను.",
    "Hindi": "क्षमा करें, इस प्रश्न के लिए पर्याप्त सत्यापित जानकारी मेरी संदर्भ लाइब्रेरी में उपलब्ध नहीं है। कृपया योजना का नाम, जिला या संबंधित विभाग बताएं। मैं पात्रता या समय-सीमा का अनुमान नहीं लगाऊंगा।",
    "Tamil": "மன்னிக்கவும், இந்தக் கேள்விக்குத் தேவையான சரிபார்க்கப்பட்ட தகவல் தற்போது எனது தகவல் தொகுப்பில் இல்லை. திட்டத்தின் பெயர், மாவட்டம் அல்லது தொடர்புடைய துறையைச் சொல்லுங்கள். தகுதி அல்லது கடைசி தேதியை நான் ஊகிக்க மாட்டேன்.",
    "English": "I could not find enough verified information for this question in my current reference library. Please share the scheme name, district or relevant department. I will not guess eligibility rules or deadlines.",
}

FOLLOW_UP_PHRASES = [
    "tell me more", "more details", "explain more", "who is eligible", "eligibility",
    "how to apply", "documents required", "application process", "ఇంకా వివరాలు",
    "మరింత వివరంగా", "అర్హత ఏమిటి", "ఎలా దరఖాస్తు", "और बताएं", "विस्तार से बताएं",
    "पात्रता क्या है", "कैसे आवेदन करें", "மேலும் விவரம்", "விரிவாக சொல்லுங்கள்",
    "தகுதி என்ன", "எப்படி விண்ணப்பிப்பது",
]


def load_knowledge():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _language_name(language):
    return LANGUAGE_NAMES.get(str(language).strip(), "English")


def _normalise(text):
    text = str(text or "").lower()
    text = text.replace("pm kisan", "pm-kisan").replace("pmkisan", "pm-kisan")
    text = re.sub(r"[^\w\s-]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def _all_records(data):
    records = []
    for section in ("schemes", "application", "grievance", "farmer", "general"):
        records.extend(data.get(section, []))
    return records


def _record_aliases(record):
    values = list(record.get("aliases", []))
    if record.get("title"):
        values.append(record["title"])
    return [_normalise(x) for x in values if _normalise(x)]


def _matching_scheme_record(query, data):
    q = _normalise(query)
    if not q:
        return None

    matches = []
    for record in data.get("schemes", []):
        for alias in _record_aliases(record):
            if len(alias) >= 3 and alias in q:
                matches.append((len(alias), record))

    return max(matches, key=lambda x: x[0])[1] if matches else None


def detect_intent(text: str) -> str:
    t = _normalise(text)
    data = load_knowledge()

    # Detect scheme names before generic farmer keywords.
    if _matching_scheme_record(t, data):
        return "schemes"

    groups = {
        "grievance": [
            "complaint", "grievance", "ఫిర్యాదు", "शिकायत",
            "புகார்", "problem", "issue", "సమస్య", "समस्या"
        ],
        "application": [
            "apply", "application", "documents", "దరఖాస్తు",
            "అప్లై", "आवेदन", "कागजात", "விண்ணப்பம்", "ஆவணம்"
        ],
        "farmer": [
            "crop", "farmer", "పంట", "రైతు", "खेती",
            "किसान", "விவசாய", "பயிர்", "soil", "irrigation", "weather"
        ],
        "schemes": [
            "scheme", "yojana", "పథకం", "యోజన",
            "सरकारी योजना", "திட்டம்", "योजना"
        ],
    }

    for intent in ("grievance", "application", "farmer", "schemes"):
        if any(term in t for term in groups[intent]):
            return intent

    return "general"


def _search_records(query, module, context=None):
    data = load_knowledge()
    q = _normalise(query)
    terms = [w for w in q.split() if len(w) > 1]

    records = list(data.get(module, [])) + list(data.get("general", []))

    named_scheme = _matching_scheme_record(query, data)

    if named_scheme:
        records = list(data.get("schemes", [])) + list(data.get("general", []))
    elif module == "general":
        records = _all_records(data)

    context_record = _matching_scheme_record(context or "", data)
    is_follow_up = (
        len(terms) <= 5
        or any(phrase in q for phrase in FOLLOW_UP_PHRASES)
    )

    if context_record and is_follow_up:
        records = [context_record]

    scored = []
    seen = set()

    for record in records:
        title = record.get("title", "")

        if title in seen:
            continue

        seen.add(title)

        haystack = _normalise(" ".join([
            title,
            record.get("keywords", ""),
            record.get("summary", ""),
            record.get("details", "")
        ]))

        score = sum(2 for term in terms if term in haystack)

        for alias in _record_aliases(record):
            if alias and alias in q:
                score += 12

        if (
            context_record
            and title == context_record.get("title")
            and is_follow_up
        ):
            score += 15

        if score:
            scored.append((score, record))

    scored.sort(key=lambda item: item[0], reverse=True)

    return [record for _, record in scored[:3]]


def _evon_generate(query, evidence, language, context=None):
    token = os.getenv("HF_TOKEN", "").strip()
    model = os.getenv("EVON_MODEL", "").strip()

    if not token or not model:
        return None

    try:
        from huggingface_hub import InferenceClient

        client = InferenceClient(model=model, token=token)

        context_text = (
            f"\nPrevious conversation context:\n{context}"
            if context else ""
        )

        result = client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are Sahaaya, a careful Indian citizen-services assistant. "
                        f"Reply ONLY in {language}. Use simple conversational language "
                        "and only the supplied evidence/context. Answer directly; do not "
                        "merely provide links. Explain purpose, possible beneficiaries, "
                        "benefits/services, application steps or documents only when "
                        "evidence supports them, and what must be verified. Never invent "
                        "amounts, eligibility, deadlines, contact numbers or live status. "
                        "If evidence is incomplete, say so. For short follow-ups, continue "
                        "discussing the same scheme. Do not claim that an application or "
                        "complaint was submitted."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Question:\n{query}{context_text}\n\n"
                        f"Reference evidence:\n{evidence}"
                    ),
                },
            ],
            max_tokens=750,
            temperature=0.15,
        )

        content = result.choices[0].message.content

        return content.strip() if content else None

    except Exception:
        return None


def answer_query(query: str, language: str, module: str = "general", context=None):
    lang = _language_name(language)

    intent = module if module != "general" else detect_intent(query)

    if intent not in {
        "schemes", "application", "grievance", "farmer", "general"
    }:
        intent = "general"

    data = load_knowledge()

    # A named scheme takes priority over the selected module.
    if _matching_scheme_record(query, data):
        intent = "schemes"

    records = _search_records(query, intent, context=context)

    evidence = "\n\n".join(
        f"TITLE: {record.get('title', '')}\n"
        f"SUMMARY: {record.get('summary', '')}\n"
        f"DETAILS: {record.get('details', '')}\n"
        f"SOURCE: {record.get('source', '')}"
        for record in records
    )

    generated = _evon_generate(
        query,
        evidence or "No matching verified evidence found.",
        lang,
        context=context
    )

    if generated:
        answer = generated

    elif records:
        sections = []

        for record in records:
            title = record.get("title", "Reference")

            summary = (
                record.get("localized", {}).get(lang)
                or LOCALIZED.get(title, {}).get(lang)
                or record.get("details")
                or record.get("summary", "")
            )

            sections.append(f"**{title}**\n{summary}")

        closing_messages = {
            "English": (
                "Check the official source for current eligibility, "
                "dates and exact requirements before taking action."
            ),
            "Telugu": (
                "చర్య తీసుకునే ముందు ప్రస్తుత అర్హత, తేదీలు మరియు "
                "ఖచ్చితమైన అవసరాలను అధికారిక వెబ్‌సైట్‌లో నిర్ధారించండి."
            ),
            "Hindi": (
                "कोई कदम उठाने से पहले वर्तमान पात्रता, तारीखें और "
                "सही आवश्यकताएं आधिकारिक वेबसाइट पर जांचें।"
            ),
            "Tamil": (
                "நடவடிக்கை எடுப்பதற்கு முன் தற்போதைய தகுதி, தேதிகள் "
                "மற்றும் தேவைகளை அதிகாரப்பூர்வ இணையதளத்தில் சரிபார்க்கவும்."
            ),
        }

        answer = (
            "\n\n".join(sections)
            + "\n\n"
            + closing_messages[lang]
        )

    else:
        answer = GENERAL_TEXT[lang]

    sources = list(dict.fromkeys(
        (record.get("title", "Official reference"), record.get("source", ""))
        for record in records
        if record.get("source")
    ))

    return answer, sources
