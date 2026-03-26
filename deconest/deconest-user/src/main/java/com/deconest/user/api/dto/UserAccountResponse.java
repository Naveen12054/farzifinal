package com.deconest.user.api.dto;

import com.deconest.user.domain.UserRole;

public record UserAccountResponse(
        Long id,
        String email,
        String fullName,
        UserRole role,
        boolean active,
        boolean verified,
        boolean blacklisted
) {
}

