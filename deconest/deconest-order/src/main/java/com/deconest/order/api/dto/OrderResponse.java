package com.deconest.order.api.dto;

import com.deconest.order.domain.OrderStatus;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

public record OrderResponse(
        Long orderId,
        String orderNumber,
        OrderStatus status,
        BigDecimal subtotal,
        BigDecimal totalAmount,
        Instant createdAt,
        ShippingAddressResponse shippingAddress,
        List<OrderItemResponse> items) {
}
