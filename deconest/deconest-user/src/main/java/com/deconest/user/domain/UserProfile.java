package com.deconest.user.domain;

import com.deconest.common.persistence.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "user_profiles")
public class UserProfile extends BaseEntity {

    @OneToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private UserAccount user;

    @Column(length = 120)
    private String country;

    @Column(length = 120)
    private String state;

    @Column(length = 120)
    private String city;

    @Column(length = 120)
    private String district;

    @Column(length = 255)
    private String addressLine1;

    @Column(length = 255)
    private String addressLine2;

    @Column(length = 20)
    private String phoneNumber;

    @Column(length = 20)
    private String alternatePhoneNumber;

    @Column(length = 12)
    private String pinCode;

    protected UserProfile() {
    }

    public UserProfile(UserAccount user) {
        this.user = user;
    }

    public UserAccount getUser() {
        return user;
    }

    public String getCountry() {
        return country;
    }

    public String getState() {
        return state;
    }

    public String getCity() {
        return city;
    }

    public String getDistrict() {
        return district;
    }

    public String getAddressLine1() {
        return addressLine1;
    }

    public String getAddressLine2() {
        return addressLine2;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public String getAlternatePhoneNumber() {
        return alternatePhoneNumber;
    }

    public String getPinCode() {
        return pinCode;
    }

    public void updateProfile(
            String country,
            String state,
            String city,
            String district,
            String addressLine1,
            String addressLine2,
            String phoneNumber,
            String alternatePhoneNumber,
            String pinCode) {
        this.country = country;
        this.state = state;
        this.city = city;
        this.district = district;
        this.addressLine1 = addressLine1;
        this.addressLine2 = addressLine2;
        this.phoneNumber = phoneNumber;
        this.alternatePhoneNumber = alternatePhoneNumber;
        this.pinCode = pinCode;
    }
}
