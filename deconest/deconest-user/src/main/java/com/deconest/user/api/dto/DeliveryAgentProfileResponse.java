package com.deconest.user.api.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import java.time.LocalDate;

public record DeliveryAgentProfileResponse(
        Long userId,
        String email,
        String fullName,
        String firstName,
        String lastName,
        String phoneNumber,
        String pinCode,
        String bankName,
        String accountHolderName,
        String accountNumber,
        String routingNumber,
        Integer maxDeliveryDistanceKm,
        @JsonFormat(pattern = "yyyy-MM-dd") LocalDate insuranceExpiryDate,
        boolean approved,
        boolean rejected) {
}
