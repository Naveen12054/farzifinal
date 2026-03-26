package com.deconest.user.domain;

import com.deconest.common.persistence.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Table;

@Entity
@Table(name = "user_accounts")
public class UserAccount extends BaseEntity {

    @Column(nullable = false, unique = true, length = 120)
    private String email;

    @Column(nullable = false, length = 120)
    private String fullName;

    @Column(nullable = false, length = 255)
    private String passwordHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 40)
    private UserRole role;

    @Column(nullable = false)
    private boolean active = true;

    @Column(nullable = false)
    private boolean verified = false;

    @Column(nullable = false)
    private boolean blacklisted = false;

    protected UserAccount() {
    }

    public UserAccount(String email, String fullName, String passwordHash, UserRole role) {
        this.email = email;
        this.fullName = fullName;
        this.passwordHash = passwordHash;
        this.role = role;
    }

    public String getEmail() {
        return email;
    }

    public String getFullName() {
        return fullName;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public UserRole getRole() {
        return role;
    }

    public boolean isActive() {
        return active;
    }

    public boolean isVerified() {
        return verified;
    }

    public boolean isBlacklisted() {
        return blacklisted;
    }

    public void markVerified() {
        this.verified = true;
    }

    public void blacklist() {
        this.blacklisted = true;
        this.active = false;
    }
}

