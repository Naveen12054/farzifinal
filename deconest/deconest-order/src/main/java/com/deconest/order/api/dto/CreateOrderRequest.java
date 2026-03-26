package com.deconest.order.api.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;

public record CreateOrderRequest(@Valid @NotNull ShippingAddressRequest shippingAddress) {
}
