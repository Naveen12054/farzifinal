package com.deconest.catalog.domain;

import com.deconest.common.persistence.BaseEntity;
import com.deconest.user.domain.UserAccount;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import java.math.BigDecimal;

@Entity
@Table(name = "catalog_products")
public class Product extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "seller_id", nullable = false)
    private UserAccount seller;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "category_id", nullable = false)
    private Category category;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "subcategory_id", nullable = false)
    private Subcategory subcategory;

    @Column(length = 120)
    private String brandName;

    @Column(nullable = false, unique = true, length = 180)
    private String name;

    @Column(length = 4000)
    private String productDescription;

    @Column(length = 2000)
    private String materialDescription;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal price;

    @Column(nullable = false)
    private Integer quantity;

    @Column(length = 255)
    private String imageUrl1;

    @Column(length = 255)
    private String imageUrl2;

    @Column(length = 255)
    private String imageUrl3;

    @Column(length = 255)
    private String imageUrl4;

    @Column(length = 255)
    private String measurements;

    @Column(length = 1000)
    private String maintenanceNotes;

    @Column(length = 120)
    private String color;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 40)
    private ProductStatus status = ProductStatus.DRAFT;

    protected Product() {
    }

    public Product(
            UserAccount seller,
            Category category,
            Subcategory subcategory,
            String brandName,
            String name,
            String productDescription,
            String materialDescription,
            BigDecimal price,
            Integer quantity,
            String imageUrl1,
            String imageUrl2,
            String imageUrl3,
            String imageUrl4,
            String measurements,
            String maintenanceNotes,
            String color,
            ProductStatus status) {
        this.seller = seller;
        this.category = category;
        this.subcategory = subcategory;
        this.brandName = brandName;
        this.name = name;
        this.productDescription = productDescription;
        this.materialDescription = materialDescription;
        this.price = price;
        this.quantity = quantity;
        this.imageUrl1 = imageUrl1;
        this.imageUrl2 = imageUrl2;
        this.imageUrl3 = imageUrl3;
        this.imageUrl4 = imageUrl4;
        this.measurements = measurements;
        this.maintenanceNotes = maintenanceNotes;
        this.color = color;
        this.status = status;
    }

    public UserAccount getSeller() {
        return seller;
    }

    public Category getCategory() {
        return category;
    }

    public Subcategory getSubcategory() {
        return subcategory;
    }

    public String getBrandName() {
        return brandName;
    }

    public String getName() {
        return name;
    }

    public String getProductDescription() {
        return productDescription;
    }

    public String getMaterialDescription() {
        return materialDescription;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public String getImageUrl1() {
        return imageUrl1;
    }

    public String getImageUrl2() {
        return imageUrl2;
    }

    public String getImageUrl3() {
        return imageUrl3;
    }

    public String getImageUrl4() {
        return imageUrl4;
    }

    public String getMeasurements() {
        return measurements;
    }

    public String getMaintenanceNotes() {
        return maintenanceNotes;
    }

    public String getColor() {
        return color;
    }

    public ProductStatus getStatus() {
        return status;
    }
}

