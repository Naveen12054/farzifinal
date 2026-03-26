package com.deconest.user.api.dto;

public record UserProfileResponse(
        Long userId,
        String email,
        String fullName,
        String country,
        String state,
        String city,
        String district,
        String addressLine1,
        String addressLine2,
        String phoneNumber,
        String alternatePhoneNumber,
        String pinCode) {
}
