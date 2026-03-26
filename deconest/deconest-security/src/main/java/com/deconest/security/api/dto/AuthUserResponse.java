package com.deconest.security.api.dto;

import com.deconest.user.domain.UserRole;

public record AuthUserResponse(
        Long id,
        String email,
        String fullName,
        UserRole role,
        boolean active,
        boolean verified
) {
}

