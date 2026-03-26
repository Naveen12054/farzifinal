package com.deconest.cart.api.dto;

import java.math.BigDecimal;

public record CartItemResponse(
        Long cartItemId,
        Long productId,
        String productName,
        String sellerName,
        BigDecimal unitPrice,
        Integer quantity,
        BigDecimal lineTotal,
        String imageUrl) {
}
