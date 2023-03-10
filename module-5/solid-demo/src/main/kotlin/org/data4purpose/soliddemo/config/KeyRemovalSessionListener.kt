package org.data4purpose.soliddemo.config

import org.data4purpose.soliddemo.dpop.DPoPUtils
import org.springframework.security.core.context.SecurityContextImpl
import org.springframework.security.web.authentication.WebAuthenticationDetails
import org.springframework.stereotype.Component
import javax.servlet.http.HttpSessionEvent
import javax.servlet.http.HttpSessionListener

@Component
class KeyRemovalSessionListener(private val dPoPUtils: DPoPUtils) : HttpSessionListener {
    override fun sessionDestroyed(se: HttpSessionEvent) {
        val sessionId = (
            (se.session.getAttribute("SPRING_SECURITY_CONTEXT") as? SecurityContextImpl)
                ?.authentication?.details as? WebAuthenticationDetails
            )?.sessionId

        sessionId?.let { dPoPUtils.removeSessionKey(it) }
    }
}
