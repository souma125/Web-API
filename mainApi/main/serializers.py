from rest_framework import serializers
from main.models import Address,Customer,Car

class CreateCustomerAddressSerializer(serializers.ModelSerializer):
    street_name = serializers.CharField(max_length=200)
    pincode = serializers.CharField(max_length=6)
    city = serializers.CharField(max_length=20)
    state = serializers.CharField(max_length=20)
    country_code = serializers.CharField(max_length=2)
    class Meta:
        model= Address
        fields= ['street_name','pincode','city','state','country_code']
    def validate(self, attrs):
        street_name = attrs.get('street_name')
        pincode = attrs.get('pincode')
        city = attrs.get('city')
        state = attrs.get('state')
        country_code = attrs.get('country_code')
        if street_name == '':
            raise serializers.ValidationError("Street name cannot be empty")
        if pincode == '':
            raise serializers.ValidationError("Pincode cannot be empty")
        if city == '':
            raise serializers.ValidationError("City cannot be empty")
        if state == '':
            raise serializers.ValidationError("state cannot be empty")
        if country_code == '' and len(country_code) < 2:
            raise serializers.ValidationError("Country code cannot be empty or not bigger than two digit")
        try:
            address = Address.objects.create(street_name=street_name,pincode=pincode,city=city,state=state,country_code=country_code)
            address.save()
        except Exception as e:
            print(e)
        return attrs
    
class CreateCarSerializer(serializers.ModelSerializer):
    model_name = serializers.ChoiceField(choices = (('modelA','modelA'),('modelB','modelB')))
    manufacturer = serializers.ChoiceField(choices = (('manufacturerA','manufacturerA'),('manufacturerB','manufacturerB')))
    color = serializers.ChoiceField(choices = (('colorA','colorA'),('colorB','colorB')))
    class Meta:
        model=Car
        fields = ['model_name','manufacturer','color']
    def validate(self, attrs):
        model_name = attrs.get('model_name')
        manufacturer = attrs.get('manufacturer')
        color = attrs.get('color')
        if model_name == '':
            raise serializers.ValidationError("Model name cannot be empty")
        if manufacturer == '':
            raise serializers.ValidationError("Manufacturer cannot be empty")
        if color == '':
            raise serializers.ValidationError("Color cannot be empty")
        
        try:
            car = Car.objects.create(model_name=model_name,manufacturer=manufacturer,color=color)
            car.save()
        except Exception as e:
            print(e)
        return attrs

        