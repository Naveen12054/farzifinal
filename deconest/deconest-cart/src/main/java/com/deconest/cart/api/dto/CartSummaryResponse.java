package com.deconest.cart.api.dto;

import java.math.BigDecimal;
import java.util.List;

public record CartSummaryResponse(
        Integer totalItems,
        BigDecimal subtotal,
        List<CartItemResponse> items) {
}
