package com.deconest.order.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

@Embeddable
public class ShippingAddress {

    @Column(name = "shipping_full_name", nullable = false, length = 120)
    private String fullName;

    @Column(name = "shipping_phone_number", nullable = false, length = 20)
    private String phoneNumber;

    @Column(name = "shipping_address_line_1", nullable = false, length = 255)
    private String addressLine1;

    @Column(name = "shipping_address_line_2", length = 255)
    private String addressLine2;

    @Column(name = "shipping_city", nullable = false, length = 120)
    private String city;

    @Column(name = "shipping_state", nullable = false, length = 120)
    private String state;

    @Column(name = "shipping_district", length = 120)
    private String district;

    @Column(name = "shipping_country", nullable = false, length = 120)
    private String country;

    @Column(name = "shipping_pin_code", nullable = false, length = 12)
    private String pinCode;

    protected ShippingAddress() {
    }

    public ShippingAddress(
            String fullName,
            String phoneNumber,
            String addressLine1,
            String addressLine2,
            String city,
            String state,
            String district,
            String country,
            String pinCode) {
        this.fullName = fullName;
        this.phoneNumber = phoneNumber;
        this.addressLine1 = addressLine1;
        this.addressLine2 = addressLine2;
        this.city = city;
        this.state = state;
        this.district = district;
        this.country = country;
        this.pinCode = pinCode;
    }

    public String getFullName() {
        return fullName;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public String getAddressLine1() {
        return addressLine1;
    }

    public String getAddressLine2() {
        return addressLine2;
    }

    public String getCity() {
        return city;
    }

    public String getState() {
        return state;
    }

    public String getDistrict() {
        return district;
    }

    public String getCountry() {
        return country;
    }

    public String getPinCode() {
        return pinCode;
    }
}
