package com.deconest.user.repository;

import com.deconest.user.domain.DeliveryAgentProfile;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DeliveryAgentProfileRepository extends JpaRepository<DeliveryAgentProfile, Long> {
    Optional<DeliveryAgentProfile> findByUserEmail(String email);
}
