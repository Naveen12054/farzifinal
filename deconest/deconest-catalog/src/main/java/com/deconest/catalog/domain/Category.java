package com.deconest.catalog.domain;

import com.deconest.common.persistence.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "catalog_categories")
public class Category extends BaseEntity {

    @Column(nullable = false, unique = true, length = 80)
    private String name;

    @Column(length = 500)
    private String description;

    @Column(length = 255)
    private String imageUrl;

    @Column(nullable = false)
    private boolean enabled = true;

    @Column(nullable = false)
    private boolean availableForSale = true;

    @Column(nullable = false)
    private boolean availableForRent = false;

    protected Category() {
    }

    public Category(String name, String description, String imageUrl, boolean availableForSale, boolean availableForRent) {
        this.name = name;
        this.description = description;
        this.imageUrl = imageUrl;
        this.availableForSale = availableForSale;
        this.availableForRent = availableForRent;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public boolean isAvailableForSale() {
        return availableForSale;
    }

    public boolean isAvailableForRent() {
        return availableForRent;
    }
}

