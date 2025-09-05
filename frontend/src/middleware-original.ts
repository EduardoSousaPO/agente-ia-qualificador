import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { createMiddlewareClient } from '@/lib/supabase'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient(req, res)

  // Refresh session if expired
  const {
    data: { session },
  } = await supabase.auth.getSession()

  // Check if this is a tenant-scoped route
  const tenantSlugMatch = req.nextUrl.pathname.match(/^\/app\/([^\/]+)/)
  
  if (tenantSlugMatch) {
    const tenantSlug = tenantSlugMatch[1]
    
    // If user is not authenticated, redirect to login
    if (!session) {
      const redirectUrl = req.nextUrl.clone()
      redirectUrl.pathname = '/login'
      redirectUrl.searchParams.set('redirectTo', req.nextUrl.pathname)
      return NextResponse.redirect(redirectUrl)
    }

    // Validate tenant access (this would typically check membership)
    // For now, we'll allow access and let the API handle authorization
    
    // Add tenant slug to headers for downstream components
    const requestHeaders = new Headers(req.headers)
    requestHeaders.set('x-tenant-slug', tenantSlug)
    
    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    })
  }

  // Handle auth routes
  if (req.nextUrl.pathname.startsWith('/login') || req.nextUrl.pathname.startsWith('/signup')) {
    // If user is already authenticated, redirect to their default tenant or dashboard
    if (session) {
      return NextResponse.redirect(new URL('/', req.url))
    }
  }

  // Protected routes (non-tenant specific)
  const protectedRoutes = ['/dashboard', '/leads', '/conversations', '/settings']
  const isProtectedRoute = protectedRoutes.some(route => 
    req.nextUrl.pathname.startsWith(route)
  )

  if (isProtectedRoute && !session) {
    const redirectUrl = req.nextUrl.clone()
    redirectUrl.pathname = '/login'
    redirectUrl.searchParams.set('redirectTo', req.nextUrl.pathname)
    return NextResponse.redirect(redirectUrl)
  }

  return res
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
