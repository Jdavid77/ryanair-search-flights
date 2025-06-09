"""
Forms for the flights app.
"""
from django import forms
from datetime import date, timedelta

CURRENCY_CHOICES = [
    ('EUR', 'EUR'),
    ('GBP', 'GBP'),
    ('USD', 'USD'),
]

TIME_RANGE_CHOICES = [
    ('ANY', 'Any time'),
    ('EARLY_MORNING', 'Early Morning (06:00 - 09:00)'),
    ('MORNING', 'Morning (09:00 - 12:00)'),
    ('AFTERNOON', 'Afternoon (12:00 - 17:00)'),
    ('EVENING', 'Evening (17:00 - 21:00)'),
    ('NIGHT', 'Night (21:00 - 06:00)'),
]

# Popular airports organized by country
AIRPORT_CHOICES = [
    ('🇵🇹 Portugal', [
        ('FNC', 'FNC - Funchal, Madeira'),
        ('LIS', 'LIS - Lisbon, Portugal'),
        ('OPO', 'OPO - Porto, Portugal'),
        ('FAO', 'FAO - Faro, Algarve'),
        ('TER', 'TER - Terceira, Azores'),
        ('PDL', 'PDL - Ponta Delgada, Azores'),
    ]),
    ('🇪🇸 Spain', [
        ('MAD', 'MAD - Madrid'),
        ('BCN', 'BCN - Barcelona'),
        ('SVQ', 'SVQ - Seville'),
        ('VLC', 'VLC - Valencia'),
        ('PMI', 'PMI - Palma, Mallorca'),
        ('IBZ', 'IBZ - Ibiza'),
        ('MAH', 'MAH - Menorca'),
        ('LPA', 'LPA - Las Palmas, Gran Canaria'),
        ('TFS', 'TFS - Tenerife South'),
        ('ACE', 'ACE - Lanzarote'),
        ('FUE', 'FUE - Fuerteventura'),
        ('BIO', 'BIO - Bilbao'),
        ('SDR', 'SDR - Santander'),
        ('VGO', 'VGO - Vigo'),
        ('SCQ', 'SCQ - Santiago de Compostela'),
        ('ALC', 'ALC - Alicante'),
        ('GRX', 'GRX - Granada'),
        ('MLG', 'MLG - Malaga'),
        ('AGP', 'AGP - Malaga Costa del Sol'),
        ('XRY', 'XRY - Jerez'),
    ]),
    ('🇬🇧 United Kingdom', [
        ('LGW', 'LGW - London Gatwick'),
        ('STN', 'STN - London Stansted'),
        ('LTN', 'LTN - London Luton'),
        ('SEN', 'SEN - London Southend'),
        ('MAN', 'MAN - Manchester'),
        ('BHX', 'BHX - Birmingham'),
        ('LPL', 'LPL - Liverpool'),
        ('BRS', 'BRS - Bristol'),
        ('EDI', 'EDI - Edinburgh'),
        ('GLA', 'GLA - Glasgow'),
        ('PIK', 'PIK - Glasgow Prestwick'),
        ('ABZ', 'ABZ - Aberdeen'),
        ('INV', 'INV - Inverness'),
        ('BFS', 'BFS - Belfast International'),
        ('BHD', 'BHD - Belfast City'),
        ('CWL', 'CWL - Cardiff'),
        ('EXT', 'EXT - Exeter'),
        ('NQY', 'NQY - Newquay Cornwall'),
        ('BOH', 'BOH - Bournemouth'),
        ('EMA', 'EMA - East Midlands'),
        ('LBA', 'LBA - Leeds Bradford'),
        ('NCL', 'NCL - Newcastle'),
        ('MME', 'MME - Teesside'),
    ]),
    ('🇮🇪 Ireland', [
        ('DUB', 'DUB - Dublin'),
        ('ORK', 'ORK - Cork'),
        ('SNN', 'SNN - Shannon'),
        ('KIR', 'KIR - Kerry'),
        ('NOC', 'NOC - Knock'),
        ('WAT', 'WAT - Waterford'),
    ]),
    ('🇫🇷 France', [
        ('CDG', 'CDG - Paris Charles de Gaulle'),
        ('ORY', 'ORY - Paris Orly'),
        ('BVA', 'BVA - Paris Beauvais'),
        ('NCE', 'NCE - Nice'),
        ('MRS', 'MRS - Marseille'),
        ('LYS', 'LYS - Lyon'),
        ('TLS', 'TLS - Toulouse'),
        ('BOD', 'BOD - Bordeaux'),
        ('NTE', 'NTE - Nantes'),
        ('MPL', 'MPL - Montpellier'),
        ('BIQ', 'BIQ - Biarritz'),
        ('CFE', 'CFE - Clermont-Ferrand'),
        ('LIG', 'LIG - Limoges'),
        ('PGF', 'PGF - Perpignan'),
        ('RNS', 'RNS - Rennes'),
        ('SXB', 'SXB - Strasbourg'),
        ('BES', 'BES - Brest'),
        ('LRH', 'LRH - La Rochelle'),
        ('PUF', 'PUF - Pau'),
        ('RDZ', 'RDZ - Rodez'),
        ('CNG', 'CNG - Cognac'),
    ]),
    ('🇮🇹 Italy', [
        ('FCO', 'FCO - Rome Fiumicino'),
        ('CIA', 'CIA - Rome Ciampino'),
        ('MXP', 'MXP - Milan Malpensa'),
        ('BGY', 'BGY - Milan Bergamo'),
        ('LIN', 'LIN - Milan Linate'),
        ('NAP', 'NAP - Naples'),
        ('BLQ', 'BLQ - Bologna'),
        ('VCE', 'VCE - Venice Marco Polo'),
        ('TSF', 'TSF - Venice Treviso'),
        ('FLR', 'FLR - Florence'),
        ('PSA', 'PSA - Pisa'),
        ('BRI', 'BRI - Bari'),
        ('CTA', 'CTA - Catania'),
        ('PMO', 'PMO - Palermo'),
        ('CAG', 'CAG - Cagliari'),
        ('AHO', 'AHO - Alghero'),
        ('TRN', 'TRN - Turin'),
        ('VRN', 'VRN - Verona'),
        ('TRS', 'TRS - Trieste'),
        ('AOI', 'AOI - Ancona'),
        ('PEG', 'PEG - Perugia'),
        ('CRV', 'CRV - Crotone'),
        ('LMP', 'LMP - Lampedusa'),
        ('SUF', 'SUF - Lamezia'),
        ('REG', 'REG - Reggio Calabria'),
        ('FOG', 'FOG - Foggia'),
        ('BDS', 'BDS - Brindisi'),
        ('TAR', 'TAR - Taranto'),
    ]),
    ('🇩🇪 Germany', [
        ('FRA', 'FRA - Frankfurt'),
        ('CGN', 'CGN - Cologne'),
        ('DUS', 'DUS - Düsseldorf'),
        ('STR', 'STR - Stuttgart'),
        ('BER', 'BER - Berlin Brandenburg'),
        ('HAM', 'HAM - Hamburg'),
        ('MUC', 'MUC - Munich'),
        ('NUE', 'NUE - Nuremberg'),
        ('HAJ', 'HAJ - Hannover'),
        ('BRE', 'BRE - Bremen'),
        ('DTM', 'DTM - Dortmund'),
        ('PAD', 'PAD - Paderborn'),
        ('SCN', 'SCN - Saarbrücken'),
        ('KSF', 'KSF - Kassel'),
        ('FDH', 'FDH - Friedrichshafen'),
        ('FMM', 'FMM - Memmingen'),
        ('HHN', 'HHN - Frankfurt Hahn'),
        ('SXF', 'SXF - Berlin Schönefeld'),
        ('WEZ', 'WEZ - Weeze'),
    ]),
    # Add other countries as needed...
]

class FlightSearchForm(forms.Form):
    departure_airport = forms.ChoiceField(
        choices=AIRPORT_CHOICES,
        initial='FNC',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'departure_airport'
        })
    )
    
    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        initial='EUR',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'currency'
        })
    )
    
    departure_date = forms.DateField(
        initial=lambda: date.today() + timedelta(days=1),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'departure_date'
        })
    )
    
    departure_end_date = forms.DateField(
        initial=lambda: date.today() + timedelta(days=15),
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'departure_end_date'
        })
    )
    
    destination_airport = forms.CharField(
        initial='ALL',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'destination_airport',
            'disabled': True
        })
    )
    
    departure_time = forms.ChoiceField(
        choices=TIME_RANGE_CHOICES,
        initial='ANY',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'departure_time'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        departure_end_date = cleaned_data.get('departure_end_date')
        
        if departure_date and departure_end_date:
            if departure_date >= departure_end_date:
                raise forms.ValidationError("End date must be after departure date.")
            
            if departure_date < date.today():
                raise forms.ValidationError("Departure date cannot be in the past.")
        
        return cleaned_data