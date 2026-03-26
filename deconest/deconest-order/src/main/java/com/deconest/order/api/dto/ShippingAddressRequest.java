package com.deconest.order.api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record ShippingAddressRequest(
        @NotBlank @Size(max = 120) String fullName,
        @NotBlank @Size(max = 20) String phoneNumber,
        @NotBlank @Size(max = 255) String addressLine1,
        @Size(max = 255) String addressLine2,
        @NotBlank @Size(max = 120) String city,
        @NotBlank @Size(max = 120) String state,
        @Size(max = 120) String district,
        @NotBlank @Size(max = 120) String country,
        @NotBlank @Size(max = 12) String pinCode) {
}
