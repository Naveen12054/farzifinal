package com.deconest.user.api.dto;

import jakarta.validation.constraints.Size;

public record UpdateUserProfileRequest(
        @Size(max = 120) String country,
        @Size(max = 120) String state,
        @Size(max = 120) String city,
        @Size(max = 120) String district,
        @Size(max = 255) String addressLine1,
        @Size(max = 255) String addressLine2,
        @Size(max = 20) String phoneNumber,
        @Size(max = 20) String alternatePhoneNumber,
        @Size(max = 12) String pinCode) {
}
