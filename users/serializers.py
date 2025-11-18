# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User # Importiere das Standard-User-Modell

class RegisterSerializer(serializers.ModelSerializer):
    # Fügen Sie ein extra Passwort-Feld hinzu, das NUR zum Schreiben (write_only=True) dient
    # und NICHT zurück an den Client gesendet wird.
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    password2 = serializers.CharField(
        write_only=True,
       required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        # Verwende das Standard-User-Modell von Django
        model = User
        # Definiere, welche Felder angenommen werden sollen
        fields = ('id', 'username', 'email', 'password', 'password2')
        # Standardmäßig benötigt Django einen 'username', 
        # aber wir können ihn hier gleich der E-Mail zuweisen:
        extra_kwargs = {'username': {'required': False}}

    # --- Validierung (Validation) ---

    def validate(self, attrs):
        # 1. Prüfe, ob die E-Mail bereits existiert
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Diese E-Mail-Adresse ist bereits registriert."})
            
        # Optional: Prüfe auf übereinstimmende Passwörter
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Die Passwörter stimmen nicht überein."})

        # Setze den Benutzernamen gleich der E-Mail ( falls Sie keinen separaten Benutzernamen wünschen )
        attrs['username'] = attrs['email']
        
        return attrs

    # --- Erstellung (Create) ---
    
    def create(self, validated_data):
        # Ruft die sichere Methode zur Erstellung des Benutzers auf.
        # WICHTIG: Die Methode create_user() sorgt dafür, dass das Passwort 
        # automatisch und sicher gehasht wird.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user