package com.deconest.user.domain;

import com.deconest.common.persistence.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import java.time.LocalDate;

@Entity
@Table(name = "delivery_agent_profiles")
public class DeliveryAgentProfile extends BaseEntity {

    @OneToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private UserAccount user;

    @Column(length = 120)
    private String firstName;

    @Column(length = 120)
    private String lastName;

    @Column(length = 20)
    private String phoneNumber;

    @Column(length = 12)
    private String pinCode;

    @Column(length = 255)
    private String bankName;

    @Column(length = 255)
    private String accountHolderName;

    @Column(length = 50)
    private String accountNumber;

    @Column(length = 50)
    private String routingNumber;

    private Integer maxDeliveryDistanceKm;

    private LocalDate insuranceExpiryDate;

    @Column(nullable = false)
    private boolean approved = false;

    @Column(nullable = false)
    private boolean rejected = false;

    protected DeliveryAgentProfile() {
    }

    public DeliveryAgentProfile(UserAccount user) {
        this.user = user;
    }

    public UserAccount getUser() {
        return user;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public String getPinCode() {
        return pinCode;
    }

    public String getBankName() {
        return bankName;
    }

    public String getAccountHolderName() {
        return accountHolderName;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public String getRoutingNumber() {
        return routingNumber;
    }

    public Integer getMaxDeliveryDistanceKm() {
        return maxDeliveryDistanceKm;
    }

    public LocalDate getInsuranceExpiryDate() {
        return insuranceExpiryDate;
    }

    public boolean isApproved() {
        return approved;
    }

    public boolean isRejected() {
        return rejected;
    }

    public void updateProfile(
            String firstName,
            String lastName,
            String phoneNumber,
            String pinCode,
            String bankName,
            String accountHolderName,
            String accountNumber,
            String routingNumber,
            Integer maxDeliveryDistanceKm,
            LocalDate insuranceExpiryDate) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.phoneNumber = phoneNumber;
        this.pinCode = pinCode;
        this.bankName = bankName;
        this.accountHolderName = accountHolderName;
        this.accountNumber = accountNumber;
        this.routingNumber = routingNumber;
        this.maxDeliveryDistanceKm = maxDeliveryDistanceKm;
        this.insuranceExpiryDate = insuranceExpiryDate;
    }
}
