package com.deconest.user.api.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

public record UpdateDeliveryAgentProfileRequest(
        @Size(max = 120) String firstName,
        @Size(max = 120) String lastName,
        @Size(max = 20) String phoneNumber,
        @Size(max = 12) String pinCode,
        @Size(max = 255) String bankName,
        @Size(max = 255) String accountHolderName,
        @Size(max = 50) String accountNumber,
        @Size(max = 50) String routingNumber,
        @Min(0) @Max(500) Integer maxDeliveryDistanceKm,
        @JsonFormat(pattern = "yyyy-MM-dd") LocalDate insuranceExpiryDate) {
}
