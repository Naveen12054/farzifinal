package com.deconest.user.api.dto;

public record SellerProfileResponse(
        Long userId,
        String email,
        String fullName,
        String ownerName,
        String gstNumber,
        String panNumber,
        String mapLocation,
        String phoneNumber,
        String alternatePhoneNumber) {
}
