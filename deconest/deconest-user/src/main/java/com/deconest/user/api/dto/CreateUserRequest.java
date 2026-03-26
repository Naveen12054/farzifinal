package com.deconest.user.api.dto;

import com.deconest.user.domain.UserRole;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record CreateUserRequest(
        @NotBlank @Email @Size(max = 120) String email,
        @NotBlank @Size(max = 120) String fullName,
        @NotBlank @Size(min = 8, max = 120) String password,
        @NotNull UserRole role
) {
}

