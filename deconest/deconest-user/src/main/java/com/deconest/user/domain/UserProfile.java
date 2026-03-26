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
}

