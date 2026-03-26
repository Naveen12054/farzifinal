package com.deconest.cart.domain;

import com.deconest.catalog.domain.Product;
import com.deconest.common.persistence.BaseEntity;
import com.deconest.user.domain.UserAccount;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;

@Entity
@Table(
        name = "wishlist_items",
        uniqueConstraints = @UniqueConstraint(name = "uk_wishlist_user_product", columnNames = {"user_id", "product_id"}))
public class WishlistItem extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "user_id", nullable = false)
    private UserAccount user;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    protected WishlistItem() {
    }

    public WishlistItem(UserAccount user, Product product) {
        this.user = user;
        this.product = product;
    }

    public UserAccount getUser() {
        return user;
    }

    public Product getProduct() {
        return product;
    }
}
