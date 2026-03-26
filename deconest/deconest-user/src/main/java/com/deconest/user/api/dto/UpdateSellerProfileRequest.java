package com.deconest.user.api.dto;

import jakarta.validation.constraints.Size;

public record UpdateSellerProfileRequest(
        @Size(max = 255) String ownerName,
        @Size(max = 150) String gstNumber,
        @Size(max = 150) String panNumber,
        @Size(max = 255) String mapLocation,
        @Size(max = 20) String phoneNumber,
        @Size(max = 20) String alternatePhoneNumber) {
}
