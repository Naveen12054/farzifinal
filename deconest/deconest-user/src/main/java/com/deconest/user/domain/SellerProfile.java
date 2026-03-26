package com.deconest.user.domain;

import com.deconest.common.persistence.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "seller_profiles")
public class SellerProfile extends BaseEntity {

    @OneToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private UserAccount user;

    @Column(length = 255)
    private String ownerName;

    @Column(length = 150)
    private String gstNumber;

    @Column(length = 150)
    private String panNumber;

    @Column(length = 255)
    private String mapLocation;

    @Column(length = 20)
    private String phoneNumber;

    @Column(length = 20)
    private String alternatePhoneNumber;

    protected SellerProfile() {
    }

    public SellerProfile(UserAccount user) {
        this.user = user;
    }

    public UserAccount getUser() {
        return user;
    }

    public String getOwnerName() {
        return ownerName;
    }

    public String getGstNumber() {
        return gstNumber;
    }

    public String getPanNumber() {
        return panNumber;
    }

    public String getMapLocation() {
        return mapLocation;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public String getAlternatePhoneNumber() {
        return alternatePhoneNumber;
    }

    public void updateProfile(
            String ownerName,
            String gstNumber,
            String panNumber,
            String mapLocation,
            String phoneNumber,
            String alternatePhoneNumber) {
        this.ownerName = ownerName;
        this.gstNumber = gstNumber;
        this.panNumber = panNumber;
        this.mapLocation = mapLocation;
        this.phoneNumber = phoneNumber;
        this.alternatePhoneNumber = alternatePhoneNumber;
    }
}
