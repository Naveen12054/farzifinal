package com.deconest.order.api.dto;

public record ShippingAddressResponse(
        String fullName,
        String phoneNumber,
        String addressLine1,
        String addressLine2,
        String city,
        String state,
        String district,
        String country,
        String pinCode) {
}
