package com.deconest.cart.api.dto;

import java.math.BigDecimal;

public record WishlistItemResponse(
        Long wishlistItemId,
        Long productId,
        String productName,
        String sellerName,
        BigDecimal unitPrice,
        String imageUrl) {
}
