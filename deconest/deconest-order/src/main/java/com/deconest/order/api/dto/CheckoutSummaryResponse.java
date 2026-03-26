package com.deconest.order.api.dto;

import java.math.BigDecimal;
import java.util.List;

public record CheckoutSummaryResponse(
        Integer totalItems,
        BigDecimal subtotal,
        List<OrderItemResponse> items) {
}
